# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""增强的FastAPI应用，集成Eko架构"""

import asyncio
import json
import logging
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk, ToolMessage, BaseMessage
from langgraph.types import Command

from ..graph.hybrid_builder import build_hybrid_graph
from ..core.event_bus import EventBus
from ..core.event_store import EventStore
from ..middleware.langgraph_middleware import LangGraphTaskTracker
from ..config import get_eko_config

# 导入原有的请求类型
from src.server.chat_request import ChatRequest, ChatMessage
from src.rag.retriever import Resource

logger = logging.getLogger(__name__)


class EkoEnhancedApp:
    """Eko增强的FastAPI应用"""
    
    def __init__(self):
        self.app = FastAPI(
            title="DeerFlow API with Eko Architecture",
            description="Enhanced API with Event-Driven Architecture",
            version="1.0.0",
        )
        
        # 初始化组件
        self.graph = None
        self.eko_components = None
        self.event_store: EventStore = None
        self.event_bus: EventBus = None
        self.task_tracker: LangGraphTaskTracker = None
        self.config = get_eko_config()
        
        # 初始化应用
        self._init_app()
        self._init_eko_components()
        self._setup_routes()
        self._setup_middleware()
    
    def _init_app(self):
        """初始化FastAPI应用"""
        # 添加CORS中间件
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        logger.info("FastAPI app initialized")
    
    def _init_eko_components(self):
        """初始化Eko组件"""
        try:
            # 构建混合图
            self.graph, self.eko_components = build_hybrid_graph(with_memory=True)
            
            if self.eko_components:
                self.event_store = self.eko_components["event_store"]
                self.event_bus = self.eko_components["event_bus"]
                self.task_tracker = self.eko_components["task_tracker"]
                
                logger.info("Eko components initialized successfully")
            else:
                logger.info("Running without Eko components")
                
        except Exception as e:
            logger.error(f"Failed to initialize Eko components: {e}")
            # 回滚到基础模式
            from src.graph.builder import build_graph_with_memory
            self.graph = build_graph_with_memory()
    
    def _setup_middleware(self):
        """设置中间件"""
        
        @self.app.middleware("http")
        async def eko_middleware(request, call_next):
            """Eko中间件，记录HTTP请求事件"""
            
            if self.config.enabled and self.event_bus:
                # 记录请求开始事件
                await self._log_request_start(request)
            
            response = await call_next(request)
            
            if self.config.enabled and self.event_bus:
                # 记录请求完成事件
                await self._log_request_complete(request, response)
            
            return response
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.post("/api/chat/stream")
        async def enhanced_chat_stream(request: ChatRequest):
            """增强的聊天流API"""
            return await self._handle_chat_stream(request)
        
        @self.app.get("/api/eko/status")
        async def eko_status():
            """获取Eko架构状态"""
            return await self._get_eko_status()
        
        @self.app.get("/api/eko/events/{thread_id}")
        async def get_thread_events(thread_id: str):
            """获取指定线程的事件"""
            return await self._get_thread_events(thread_id)
        
        @self.app.get("/api/eko/metrics")
        async def get_metrics():
            """获取Eko架构指标"""
            return await self._get_metrics()
        
        @self.app.post("/api/eko/replay/{thread_id}")
        async def replay_events(thread_id: str):
            """重放指定线程的事件"""
            return await self._replay_events(thread_id)
    
    async def _handle_chat_stream(self, request: ChatRequest):
        """处理聊天请求"""
        
        thread_id = request.thread_id
        if thread_id == "__default__":
            thread_id = str(uuid4())
        
        # 开始任务跟踪
        if self.task_tracker:
            user_message = request.messages[-1]['content'] if request.messages else ""
            await self.task_tracker.start_task(thread_id, user_message)
        
        return StreamingResponse(
            self._astream_workflow_generator(
                request.messages,
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
        self,
        messages: List[ChatMessage],
        thread_id: str,
        resources: List[Resource],
        max_plan_iterations: int,
        max_step_num: int,
        max_search_results: int,
        auto_accepted_plan: bool,
        interrupt_feedback: str,
        mcp_settings: dict,
        enable_background_investigation: bool,
    ):
        """增强的工作流生成器，支持Eko事件"""
        
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
            if messages:
                resume_msg += f" {messages[-1]['content']}"
            input_ = Command(resume=resume_msg)
        
        # 创建事件订阅队列
        event_queue = asyncio.Queue() if self.config.enabled else None
        
        # 订阅Eko事件
        if self.event_bus and event_queue:
            await self._subscribe_to_events(thread_id, event_queue)
        
        try:
            # 启动LangGraph流
            langgraph_task = asyncio.create_task(
                self._process_langgraph_stream(
                    input_, thread_id, resources, max_plan_iterations,
                    max_step_num, max_search_results, mcp_settings
                )
            )
            
            # 并行处理LangGraph事件和Eko事件
            while not langgraph_task.done():
                # 优先处理Eko事件
                if event_queue:
                    try:
                        eko_event = await asyncio.wait_for(event_queue.get(), timeout=0.1)
                        yield eko_event
                    except asyncio.TimeoutError:
                        pass
                
                # 处理LangGraph事件
                if langgraph_task.done():
                    break
                
                await asyncio.sleep(0.01)  # 防止CPU占用过高
            
            # 获取最终结果
            if langgraph_task.done():
                try:
                    async for event in langgraph_task.result():
                        yield event
                except Exception as e:
                    logger.error(f"Error processing LangGraph stream: {e}")
        
        finally:
            # 完成任务跟踪
            if self.task_tracker:
                await self.task_tracker.complete_task(thread_id)
    
    async def _process_langgraph_stream(
        self, input_, thread_id, resources, max_plan_iterations,
        max_step_num, max_search_results, mcp_settings
    ):
        """处理LangGraph流"""
        
        async def stream_generator():
            async for agent, _, event_data in self.graph.astream(
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
                yield self._make_langgraph_event(agent, event_data, thread_id)
        
        return stream_generator()
    
    async def _subscribe_to_events(self, thread_id: str, event_queue: asyncio.Queue):
        """订阅Eko事件"""
        
        async def event_handler(event):
            if event.metadata.correlationId == thread_id:
                sse_data = {
                    "type": "eko_event",
                    "event_type": event.type,
                    "data": event.payload,
                    "timestamp": event.timestamp,
                    "correlation_id": event.metadata.correlationId
                }
                
                await event_queue.put(
                    f"event: eko_event\ndata: {json.dumps(sse_data, ensure_ascii=False)}\n\n"
                )
        
        # 订阅所有事件类型
        from ..core.event_store import EventTypes
        for event_type in [
            EventTypes.RESEARCH_TASK_CREATED,
            EventTypes.AGENT_STARTED,
            EventTypes.AGENT_COMPLETED,
            EventTypes.SEARCH_COMPLETED,
            EventTypes.CONTENT_PROCESSED
        ]:
            self.event_bus.subscribe(event_type, event_handler)
    
    def _make_langgraph_event(self, agent, event_data, thread_id: str):
        """创建LangGraph事件"""
        
        if isinstance(event_data, dict):
            if "__interrupt__" in event_data:
                return f"event: interrupt\ndata: {json.dumps({
                    'thread_id': thread_id,
                    'id': event_data['__interrupt__'][0].ns[0],
                    'role': 'assistant',
                    'content': event_data['__interrupt__'][0].value,
                    'finish_reason': 'interrupt',
                    'options': [
                        {'text': 'Edit plan', 'value': 'edit_plan'},
                        {'text': 'Start research', 'value': 'accepted'},
                    ],
                }, ensure_ascii=False)}\n\n"
            return ""
        
        message_chunk, message_metadata = event_data
        event_stream_message = {
            "thread_id": thread_id,
            "agent": agent[0].split(":")[0],
            "id": message_chunk.id,
            "role": "assistant",
            "content": message_chunk.content,
        }
        
        if message_chunk.response_metadata.get("finish_reason"):
            event_stream_message["finish_reason"] = message_chunk.response_metadata.get("finish_reason")
        
        if isinstance(message_chunk, ToolMessage):
            event_stream_message["tool_call_id"] = message_chunk.tool_call_id
            return f"event: tool_call_result\ndata: {json.dumps(event_stream_message, ensure_ascii=False)}\n\n"
        elif isinstance(message_chunk, AIMessageChunk):
            if message_chunk.tool_calls:
                event_stream_message["tool_calls"] = message_chunk.tool_calls
                event_stream_message["tool_call_chunks"] = message_chunk.tool_call_chunks
                return f"event: tool_calls\ndata: {json.dumps(event_stream_message, ensure_ascii=False)}\n\n"
            elif message_chunk.tool_call_chunks:
                event_stream_message["tool_call_chunks"] = message_chunk.tool_call_chunks
                return f"event: tool_call_chunks\ndata: {json.dumps(event_stream_message, ensure_ascii=False)}\n\n"
            else:
                return f"event: message_chunk\ndata: {json.dumps(event_stream_message, ensure_ascii=False)}\n\n"
        
        return ""
    
    async def _get_eko_status(self):
        """获取Eko状态"""
        
        if not self.config.enabled:
            return {"status": "disabled", "message": "Eko architecture is disabled"}
        
        return {
            "status": "enabled",
            "components": {
                "event_store": "active" if self.event_store else "inactive",
                "event_bus": "active" if self.event_bus else "inactive",
                "task_tracker": "active" if self.task_tracker else "inactive",
            },
            "config": {
                "event_store_type": self.config.event_store_type,
                "event_bus_type": self.config.event_bus_type,
                "debug_mode": self.config.debug_mode,
            }
        }
    
    async def _get_thread_events(self, thread_id: str):
        """获取线程事件"""
        
        if not self.event_store:
            raise HTTPException(status_code=503, detail="Event store not available")
        
        try:
            events = self.event_store.getEvents(thread_id)
            return {
                "thread_id": thread_id,
                "event_count": len(events),
                "events": [
                    {
                        "id": event.id,
                        "type": event.type,
                        "timestamp": event.timestamp,
                        "payload": event.payload,
                    }
                    for event in events
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get events: {e}")
    
    async def _get_metrics(self):
        """获取指标"""
        
        if not self.eko_components:
            return {"metrics": "unavailable", "reason": "Eko components not initialized"}
        
        # 这里可以添加更多指标收集逻辑
        return {
            "active_tasks": len(self.task_tracker.get_active_tasks()) if self.task_tracker else 0,
            "total_events": len(self.event_store.events) if self.event_store else 0,
            "config": {
                "enabled": self.config.enabled,
                "debug_mode": self.config.debug_mode,
            }
        }
    
    async def _replay_events(self, thread_id: str):
        """重放事件"""
        
        if not self.event_store:
            raise HTTPException(status_code=503, detail="Event store not available")
        
        try:
            events = self.event_store.getEvents(thread_id)
            return {
                "thread_id": thread_id,
                "replayed_events": len(events),
                "message": f"Replayed {len(events)} events for thread {thread_id}"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to replay events: {e}")
    
    async def _log_request_start(self, request):
        """记录请求开始"""
        # 实现请求开始日志
        pass
    
    async def _log_request_complete(self, request, response):
        """记录请求完成"""
        # 实现请求完成日志
        pass


# 创建应用实例
def create_eko_app() -> FastAPI:
    """创建Eko增强的FastAPI应用"""
    eko_app = EkoEnhancedApp()
    return eko_app.app


# 便捷函数
app = create_eko_app() 