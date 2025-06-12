# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import asyncio
import base64
import json
import logging
import os
from typing import Annotated, List, cast
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from langchain_core.messages import AIMessageChunk, ToolMessage, BaseMessage
from langgraph.types import Command

from src.config.tools import SELECTED_RAG_PROVIDER
from src.graph.builder import build_graph_with_memory, get_eko_components
from src.podcast.graph.builder import build_graph as build_podcast_graph
try:
    from src.ppt.graph.builder import build_graph as build_ppt_graph
    PPT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PPT module not available: {e}")
    PPT_AVAILABLE = False
    def build_ppt_graph():
        raise ImportError("PPT functionality requires python-pptx. Install with: pip install python-pptx")

try:
    from src.pdf.generator import generate_report_pdf
    PDF_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PDF module not available: {e}")
    PDF_AVAILABLE = False
    def generate_report_pdf(content, title):
        raise ImportError("PDF functionality requires reportlab. Install with: pip install reportlab")
from src.prose.graph.builder import build_graph as build_prose_graph
from src.rag.builder import build_retriever
from src.rag.retriever import Resource
from src.server.chat_request import (
    ChatMessage,
    ChatRequest,
    GeneratePodcastRequest,
    GeneratePPTRequest,
    GenerateProseRequest,
    GeneratePDFRequest,
    TTSRequest,
)
from src.server.mcp_request import MCPServerMetadataRequest, MCPServerMetadataResponse
from src.server.mcp_utils import load_mcp_tools
from src.server.rag_request import (
    RAGConfigResponse,
    RAGResourceRequest,
    RAGResourcesResponse,
)
from src.tools import VolcengineTTS

logger = logging.getLogger(__name__)

INTERNAL_SERVER_ERROR_DETAIL = "Internal Server Error"

# 尝试导入Eko框架
try:
    from src.eko import is_eko_enabled, get_eko_config
    EKO_AVAILABLE = True
    logger.info("✅ Eko framework is available for server")
except ImportError:
    EKO_AVAILABLE = False
    logger.info("⚠️ Eko framework not available for server")
    
    def is_eko_enabled():
        return False
    
    def get_eko_config():
        return None

app = FastAPI(
    title="DeerFlow API" + (" with Eko" if EKO_AVAILABLE and is_eko_enabled() else ""),
    description="API for DeerFlow" + (" enhanced with Event-Driven Architecture" if EKO_AVAILABLE and is_eko_enabled() else ""),
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 构建图（现在支持Eko增强）
graph = build_graph_with_memory()
eko_components = get_eko_components(graph)

# 如果启用了Eko，记录组件信息
if eko_components:
    logger.info("🎯 Eko components loaded:")
    logger.info(f"   - Event Store: {type(eko_components['event_store']).__name__}")
    logger.info(f"   - Event Bus: {type(eko_components['event_bus']).__name__}")
    logger.info(f"   - Middleware: {type(eko_components['middleware']).__name__}")
    logger.info(f"   - Task Tracker: {type(eko_components['task_tracker']).__name__}")


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    thread_id = request.thread_id
    if thread_id == "__default__":
        thread_id = str(uuid4())
    
    # 如果启用了Eko，启动任务追踪
    if eko_components and eko_components.get("task_tracker"):
        try:
            user_message = request.messages[-1]['content'] if request.messages else "Unknown query"
            await eko_components["task_tracker"].start_task(thread_id, user_message)
            logger.debug(f"🎯 Started Eko task tracking for thread: {thread_id}")
        except Exception as e:
            logger.warning(f"Failed to start Eko task tracking: {e}")
    
    return StreamingResponse(
        _astream_workflow_generator(
            request.model_dump()["messages"],
            thread_id,
            request.resources,
            request.max_plan_iterations,
            request.max_step_num,
            request.max_search_results,
            request.auto_accepted_plan,
            request.interrupt_feedback,
            request.mcp_settings,
            request.enable_background_investigation,
        ),
        media_type="text/event-stream",
    )


async def _astream_workflow_generator(
    messages: List[ChatMessage],
    thread_id: str,
    resources: List[Resource],
    max_plan_iterations: int,
    max_step_num: int,
    max_search_results: int,
    auto_accepted_plan: bool,
    interrupt_feedback: str,
    mcp_settings: dict,
    enable_background_investigation,
):
    input_ = {
        "messages": messages,
        "plan_iterations": 0,
        "final_report": "",
        "current_plan": None,
        "observations": [],
        "auto_accepted_plan": auto_accepted_plan,
        "enable_background_investigation": enable_background_investigation,
    }
    if not auto_accepted_plan and interrupt_feedback:
        resume_msg = f"[{interrupt_feedback}]"
        # add the last message to the resume message
        if messages:
            resume_msg += f" {messages[-1]['content']}"
        input_ = Command(resume=resume_msg)
    
    task_completed = False
    final_report = None
    
    async for agent, _, event_data in graph.astream(
        input_,
        config={
            "thread_id": thread_id,
            "resources": resources,
            "max_plan_iterations": max_plan_iterations,
            "max_step_num": max_step_num,
            "max_search_results": max_search_results,
            "mcp_settings": mcp_settings,
        },
        stream_mode=["messages", "updates"],
        subgraphs=True,
    ):
        if isinstance(event_data, dict):
            if "__interrupt__" in event_data:
                yield _make_event(
                    "interrupt",
                    {
                        "thread_id": thread_id,
                        "id": event_data["__interrupt__"][0].ns[0],
                        "role": "assistant",
                        "content": event_data["__interrupt__"][0].value,
                        "finish_reason": "interrupt",
                        "options": [
                            {"text": "Edit plan", "value": "edit_plan"},
                            {"text": "Start research", "value": "accepted"},
                        ],
                    },
                )
            continue
        message_chunk, message_metadata = cast(
            tuple[BaseMessage, dict[str, any]], event_data
        )
        event_stream_message: dict[str, any] = {
            "thread_id": thread_id,
            "agent": agent[0].split(":")[0],
            "id": message_chunk.id,
            "role": "assistant",
            "content": message_chunk.content,
        }
        if message_chunk.response_metadata.get("finish_reason"):
            event_stream_message["finish_reason"] = message_chunk.response_metadata.get(
                "finish_reason"
            )
            # 检查是否是任务完成
            if message_chunk.response_metadata.get("finish_reason") == "stop" and agent[0] == "reporter":
                task_completed = True
                final_report = message_chunk.content
        
        if isinstance(message_chunk, ToolMessage):
            # Tool Message - Return the result of the tool call
            event_stream_message["tool_call_id"] = message_chunk.tool_call_id
            yield _make_event("tool_call_result", event_stream_message)
        elif isinstance(message_chunk, AIMessageChunk):
            # AI Message - Raw message tokens
            if message_chunk.tool_calls:
                # AI Message - Tool Call
                event_stream_message["tool_calls"] = message_chunk.tool_calls
                event_stream_message["tool_call_chunks"] = (
                    message_chunk.tool_call_chunks
                )
                yield _make_event("tool_calls", event_stream_message)
            elif message_chunk.tool_call_chunks:
                # AI Message - Tool Call Chunks
                event_stream_message["tool_call_chunks"] = (
                    message_chunk.tool_call_chunks
                )
                yield _make_event("tool_call_chunks", event_stream_message)
            else:
                # AI Message - Raw message tokens
                yield _make_event("message_chunk", event_stream_message)
    
    # 如果启用了Eko且任务完成，完成任务追踪
    if task_completed and eko_components and eko_components.get("task_tracker"):
        try:
            await eko_components["task_tracker"].complete_task(thread_id, final_report)
            logger.debug(f"🎯 Completed Eko task tracking for thread: {thread_id}")
        except Exception as e:
            logger.warning(f"Failed to complete Eko task tracking: {e}")


def _make_event(event_type: str, data: dict[str, any]):
    if data.get("content") == "":
        data.pop("content")
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


# ==== Eko API 端点 ====
if EKO_AVAILABLE and is_eko_enabled():
    
    @app.get("/api/eko/status")
    async def eko_status():
        """获取Eko架构状态"""
        if not eko_components:
            return {"status": "disabled", "message": "Eko components not initialized"}
        
        config = get_eko_config()
        return {
            "status": "enabled",
            "message": "Eko Event-Driven Architecture is active",
            "config": {
                "event_store_type": config.event_store_type,
                "event_bus_type": config.event_bus_type,
                "langgraph_compat": config.langgraph_compat,
                "debug_mode": config.debug_mode,
                "metrics_enabled": config.metrics_enabled,
            },
            "components": {
                "event_store": type(eko_components["event_store"]).__name__,
                "event_bus": type(eko_components["event_bus"]).__name__,
                "middleware": type(eko_components["middleware"]).__name__,
                "task_tracker": type(eko_components["task_tracker"]).__name__,
            }
        }

    @app.get("/api/eko/events/{thread_id}")
    async def get_eko_events(thread_id: str):
        """获取指定线程的事件历史"""
        if not eko_components or not eko_components.get("event_store"):
            raise HTTPException(status_code=503, detail="Eko event store not available")
        
        try:
            events = eko_components["event_store"].getEvents(thread_id)
            return {
                "thread_id": thread_id,
                "event_count": len(events),
                "events": [
                    {
                        "id": event.id,
                        "type": event.type,
                        "timestamp": event.timestamp,
                        "payload": event.payload,
                        "metadata": {
                            "correlationId": event.metadata.correlationId,
                            "source": event.metadata.source,
                            "userId": event.metadata.userId,
                        }
                    }
                    for event in events
                ]
            }
        except Exception as e:
            logger.error(f"Failed to get events for thread {thread_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve events")

    @app.get("/api/eko/metrics")
    async def eko_metrics():
        """获取Eko架构指标"""
        if not eko_components:
            return {"metrics": "unavailable", "reason": "Eko components not initialized"}
        
        try:
            all_events = eko_components["event_store"].getAllEvents()
            active_tasks = eko_components["task_tracker"].get_active_tasks()
            
            return {
                "total_events": len(all_events),
                "active_tasks": len(active_tasks),
                "event_types": _count_event_types(all_events),
                "system_status": "healthy"
            }
        except Exception as e:
            logger.error(f"Failed to get Eko metrics: {e}")
            return {"metrics": "error", "reason": str(e)}

    def _count_event_types(events):
        """统计事件类型"""
        counts = {}
        for event in events:
            counts[event.type] = counts.get(event.type, 0) + 1
        return counts

else:
    logger.info("ℹ️ Eko API endpoints not available (Eko framework disabled)")


# ==== 传统API端点 ====

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using volcengine TTS API."""
    try:
        app_id = os.getenv("VOLCENGINE_TTS_APPID", "")
        if not app_id:
            raise HTTPException(
                status_code=400, detail="VOLCENGINE_TTS_APPID is not set"
            )
        access_token = os.getenv("VOLCENGINE_TTS_ACCESS_TOKEN", "")
        if not access_token:
            raise HTTPException(
                status_code=400, detail="VOLCENGINE_TTS_ACCESS_TOKEN is not set"
            )
        cluster = os.getenv("VOLCENGINE_TTS_CLUSTER", "volcano_tts")

        tts = VolcengineTTS(
            app_id=app_id, access_token=access_token, cluster=cluster
        )
        audio = await tts.asynthesize(
            voice_type=request.voice_type, text=request.text
        )

        # Encode audio as base64
        audio_base64 = base64.b64encode(audio).decode("utf-8")

        return Response(
            content=audio,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3",
                "X-Audio-Base64": audio_base64,
            },
        )
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.post("/api/podcast/generate")
async def generate_podcast(request: GeneratePodcastRequest):
    """Generate podcast based on a topic or document content."""
    try:
        podcast_graph = build_podcast_graph()
        result = await podcast_graph.ainvoke(
            {"topic_or_content": request.content}
        )

        return {"podcast_script": result["podcast_script"]}
    except Exception as e:
        logger.error(f"Error in generate_podcast: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.post("/api/ppt/generate")
async def generate_ppt(request: GeneratePPTRequest):
    """Generate PowerPoint presentation based on a topic."""
    try:
        logger.info(f"Generating PPT for topic: {request.topic}")
        
        if not PPT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="PPT generation unavailable. Missing dependency: python-pptx. Install with: pip install python-pptx"
            )
        
        # 添加超时处理
        try:
            ppt_graph = build_ppt_graph()
            
            # 使用asyncio.wait_for添加超时
            result = await asyncio.wait_for(
                ppt_graph.ainvoke({"input": request.topic}),
                timeout=120.0  # 2分钟超时
            )
        except asyncio.TimeoutError:
            logger.error("PPT generation timed out")
            raise HTTPException(
                status_code=504,
                detail="PPT generation timed out. Please try with a simpler topic."
            )

        # Get the generated file path
        file_path = result.get("generated_file_path", "")
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=500,
                detail="PPT file was not generated successfully"
            )
        
        # Read the PPT file and return as binary response
        with open(file_path, "rb") as f:
            ppt_content = f.read()
        
        # Generate a filename based on the topic
        safe_topic = "".join(c for c in request.topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_topic[:50]}.pptx" if safe_topic else "presentation.pptx"
        
        return Response(
            content=ppt_content,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )
    except HTTPException:
        raise
    except ImportError as e:
        logger.error(f"PPT dependency error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"PPT generation unavailable: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"Error in generate_ppt: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.post("/api/prose/generate")
async def generate_prose(request: GenerateProseRequest):
    """Generate prose based on a topic or existing content."""
    try:
        logger.info(f"Generating prose for: {request.prompt[:100]}...")
        
        prose_graph = build_prose_graph()
        
        # Map prompt to content field expected by prose graph
        input_data = {"content": request.prompt, "option": request.option, "command": request.command}
        
        result = await prose_graph.ainvoke(input_data)
        
        return {"prose": result.get("prose", "")}
    except Exception as e:
        logger.error(f"Error in generate_prose: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.post("/api/pdf/generate")
async def generate_pdf_report(request: GeneratePDFRequest):
    """Generate PDF report from markdown content."""
    try:
        logger.info(f"Generating PDF report: {request.title}")
        
        if not PDF_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="PDF generation unavailable. Missing dependency: reportlab. Install with: pip install reportlab"
            )
        
        # 添加超时处理
        try:
            # 使用asyncio.wait_for添加超时
            pdf_path = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, generate_report_pdf, request.content, request.title
                ),
                timeout=60.0  # 1分钟超时
            )
        except asyncio.TimeoutError:
            logger.error("PDF generation timed out")
            raise HTTPException(
                status_code=504,
                detail="PDF generation timed out. Please try with shorter content."
            )

        # 验证文件是否生成成功
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=500,
                detail="PDF file was not generated successfully"
            )
        
        # 读取PDF文件并返回为二进制响应
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        
        # 生成文件名
        safe_title = "".join(c for c in request.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title[:50]}.pdf" if safe_title else "report.pdf"
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )
    except HTTPException:
        raise
    except ImportError as e:
        logger.error(f"PDF dependency error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"PDF generation unavailable: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"Error in generate_pdf_report: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.post("/api/mcp/server/metadata", response_model=MCPServerMetadataResponse)
async def mcp_server_metadata(request: MCPServerMetadataRequest):
    """Get metadata for MCP servers and tools."""
    try:
        # Load available MCP tools
        mcp_tools = load_mcp_tools()
        
        # Find the requested server
        server_config = None
        for server_name, config in mcp_tools.items():
            if server_name == request.server_name:
                server_config = config
                break
        
        if not server_config:
            raise HTTPException(
                status_code=404, 
                detail=f"MCP server '{request.server_name}' not found"
            )
        
        # Extract tools metadata
        tools_metadata = []
        if "tools" in server_config:
            for tool in server_config["tools"]:
                tools_metadata.append({
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {}).get("properties", {})
                })
        
        return MCPServerMetadataResponse(
            server_name=request.server_name,
            tools=tools_metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in mcp_server_metadata: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e


@app.get("/api/rag/config", response_model=RAGConfigResponse)
async def rag_config():
    """Get RAG configuration."""
    return RAGConfigResponse(provider=SELECTED_RAG_PROVIDER)


@app.get("/api/rag/resources", response_model=RAGResourcesResponse)
async def rag_resources(request: Annotated[RAGResourceRequest, Query()]):
    """Get RAG resources based on query."""
    try:
        if not SELECTED_RAG_PROVIDER:
            return RAGResourcesResponse(resources=[])

        retriever = build_retriever(SELECTED_RAG_PROVIDER)
        results = await retriever.asearch(request.query, k=request.k)
        
        return RAGResourcesResponse(resources=results)
    except Exception as e:
        logger.error(f"Error in rag_resources: {str(e)}")
        raise HTTPException(
            status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL
        ) from e
