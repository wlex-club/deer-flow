# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import asyncio
import logging
from src.graph import build_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """Enable debug level logging for more detailed execution information."""
    logging.getLogger("src").setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

# 尝试导入Eko框架
try:
    from src.eko import is_eko_enabled
    EKO_AVAILABLE = True
    
    if is_eko_enabled():
        logger.info("🚀 Eko Event-Driven Architecture is enabled for CLI mode")
    else:
        logger.info("🔧 Running CLI in traditional mode")
        
except ImportError:
    EKO_AVAILABLE = False
    logger.info("⚠️ Eko framework not available for CLI mode")
    
    def is_eko_enabled():
        return False

# Create the graph (now supports Eko enhancement)
graph = build_graph()

# 如果启用了Eko，获取组件
eko_components = None
if EKO_AVAILABLE and is_eko_enabled():
    from src.graph.builder import get_eko_components
    eko_components = get_eko_components(graph)
    if eko_components:
        logger.info("🎯 Eko components available for CLI:")
        logger.info(f"   - Event Store: {type(eko_components['event_store']).__name__}")
        logger.info(f"   - Task Tracker: {type(eko_components['task_tracker']).__name__}")


async def run_agent_workflow_async(
    user_input: str,
    debug: bool = False,
    max_plan_iterations: int = 1,
    max_step_num: int = 3,
    enable_background_investigation: bool = True,
):
    """Run the agent workflow asynchronously with the given user input.

    Args:
        user_input: The user's query or request
        debug: If True, enables debug level logging
        max_plan_iterations: Maximum number of plan iterations
        max_step_num: Maximum number of steps in a plan
        enable_background_investigation: If True, performs web search before planning to enhance context

    Returns:
        The final state after the workflow completes
    """
    if not user_input:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting async workflow with user input: {user_input}")
    
    # 如果启用了Eko，开始任务追踪
    thread_id = "cli_default"
    if eko_components and eko_components.get("task_tracker"):
        try:
            await eko_components["task_tracker"].start_task(thread_id, user_input)
            logger.debug(f"🎯 Started Eko task tracking for CLI session: {thread_id}")
        except Exception as e:
            logger.warning(f"Failed to start Eko task tracking: {e}")
    
    initial_state = {
        # Runtime Variables
        "messages": [{"role": "user", "content": user_input}],
        "auto_accepted_plan": True,
        "enable_background_investigation": enable_background_investigation,
    }
    config = {
        "configurable": {
            "thread_id": thread_id,
            "max_plan_iterations": max_plan_iterations,
            "max_step_num": max_step_num,
            "mcp_settings": {
                "servers": {
                    "mcp-github-trending": {
                        "transport": "stdio",
                        "command": "uvx",
                        "args": ["mcp-github-trending"],
                        "enabled_tools": ["get_github_trending_repositories"],
                        "add_to_agents": ["researcher"],
                    }
                }
            },
        },
        "recursion_limit": 100,
    }
    
    last_message_cnt = 0
    final_report = None
    task_completed = False
    
    async for s in graph.astream(
        input=initial_state, config=config, stream_mode="values"
    ):
        try:
            if isinstance(s, dict) and "messages" in s:
                if len(s["messages"]) <= last_message_cnt:
                    continue
                last_message_cnt = len(s["messages"])
                message = s["messages"][-1]
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()
                    
                # 检查是否是最终报告（任务完成）
                if (hasattr(message, 'content') and 
                    s.get("final_report") and 
                    len(s.get("final_report", "")) > 0):
                    task_completed = True
                    final_report = s.get("final_report")
            else:
                # For any other output format
                print(f"Output: {s}")
                
        except Exception as e:
            logger.error(f"Error processing stream output: {e}")
            print(f"Error processing output: {str(e)}")

    # 如果启用了Eko且任务完成，完成任务追踪
    if task_completed and eko_components and eko_components.get("task_tracker"):
        try:
            await eko_components["task_tracker"].complete_task(thread_id, final_report)
            logger.debug(f"🎯 Completed Eko task tracking for CLI session: {thread_id}")
        except Exception as e:
            logger.warning(f"Failed to complete Eko task tracking: {e}")

    logger.info("Async workflow completed successfully")


def show_eko_status():
    """显示Eko状态信息（用于CLI调试）"""
    if not EKO_AVAILABLE:
        print("❌ Eko framework is not available")
        return
        
    if not is_eko_enabled():
        print("🔧 Eko framework is available but disabled")
        print("   Set EKO_ENABLED=true to enable")
        return
        
    print("✅ Eko Event-Driven Architecture is ENABLED")
    print("🎯 CLI Mode Features:")
    print("   - Task lifecycle tracking")
    print("   - Event sourcing for audit trail")
    print("   - Performance metrics collection")
    
    if eko_components:
        print("📊 Available Components:")
        for name, component in eko_components.items():
            print(f"   - {name}: {type(component).__name__}")


if __name__ == "__main__":
    # 如果直接运行此脚本，显示图表和Eko状态
    print("🦌 DeerFlow Workflow Graph")
    print("=" * 50)
    
    # 显示Eko状态
    show_eko_status()
    print()
    
    # 显示图表
    print("📊 Workflow Graph (Mermaid):")
    print("-" * 30)
    print(graph.get_graph(xray=True).draw_mermaid())
