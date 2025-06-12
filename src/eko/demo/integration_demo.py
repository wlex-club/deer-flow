# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""Eko架构集成演示"""

import asyncio
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EkoIntegrationDemo:
    """Eko架构集成演示"""
    
    def __init__(self):
        self.graph = None
        self.eko_components = None
        self.event_store = None
        self.event_bus = None
        self.task_tracker = None
    
    async def initialize(self):
        """初始化演示环境"""
        logger.info("Initializing Eko Integration Demo...")
        
        try:
            # 构建混合图
            from ..graph.hybrid_builder import build_hybrid_graph
            self.graph, self.eko_components = build_hybrid_graph(with_memory=True)
            
            if self.eko_components:
                self.event_store = self.eko_components["event_store"]
                self.event_bus = self.eko_components["event_bus"]
                self.task_tracker = self.eko_components["task_tracker"]
                
                # 订阅事件以便监控
                await self._setup_event_monitoring()
                
                logger.info("✅ Eko components initialized successfully")
                return True
            else:
                logger.warning("⚠️ Running without Eko components")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {e}")
            return False
    
    async def _setup_event_monitoring(self):
        """设置事件监控"""
        
        async def log_event(event):
            logger.info(f"🔔 Event: {event.type} | Task: {event.metadata.correlationId}")
            logger.debug(f"   Payload: {event.payload}")
        
        # 订阅所有事件类型
        from ..core.event_store import EventTypes
        for event_type in [
            EventTypes.RESEARCH_TASK_CREATED,
            EventTypes.AGENT_STARTED,
            EventTypes.AGENT_COMPLETED,
            EventTypes.SEARCH_COMPLETED,
            EventTypes.CONTENT_PROCESSED
        ]:
            self.event_bus.subscribe(event_type, log_event)
    
    async def demo_basic_research_flow(self):
        """演示基本研究流程"""
        logger.info("\n" + "="*50)
        logger.info("🚀 Running Basic Research Flow Demo")
        logger.info("="*50)
        
        thread_id = "demo_basic_001"
        query = "What are the latest trends in AI research?"
        
        # 开始任务跟踪
        if self.task_tracker:
            await self.task_tracker.start_task(thread_id, query)
        
        # 构建输入
        input_data = {
            "messages": [{"role": "user", "content": query}],
            "plan_iterations": 0,
            "final_report": "",
            "current_plan": None,
            "observations": [],
            "auto_accepted_plan": True,  # 自动接受计划
            "enable_background_investigation": False,  # 简化演示
        }
        
        try:
            # 运行图
            logger.info(f"📝 Processing query: {query}")
            
            result = None
            count = 0
            async for chunk in self.graph.astream(
                input_data,
                config={
                    "thread_id": thread_id,
                    "max_plan_iterations": 1,
                    "max_step_num": 1,
                    "max_search_results": 2,
                },
                stream_mode=["updates"]
            ):
                result = chunk
                count += 1
                logger.info(f"📊 Graph update {count}: {list(chunk.keys())}")
                
                # 限制输出以防无限循环
                if count > 10:
                    logger.info("🛑 Limiting demo output")
                    break
            
            # 显示结果
            if result:
                logger.info(f"📄 Demo completed with {count} updates")
            
            # 完成任务跟踪
            if self.task_tracker:
                final_report = result.get("final_report", "") if result else ""
                await self.task_tracker.complete_task(thread_id, final_report)
            
            # 显示事件统计
            await self._show_event_statistics(thread_id)
            
        except Exception as e:
            logger.error(f"❌ Error in demo: {e}")
            import traceback
            traceback.print_exc()
    
    async def _show_event_statistics(self, thread_id: str):
        """显示事件统计"""
        if not self.event_store:
            return
        
        events = self.event_store.getEvents(thread_id)
        logger.info(f"📊 Event Statistics for {thread_id}:")
        logger.info(f"   Total Events: {len(events)}")
        
        if events:
            start_time = min(event.timestamp for event in events)
            end_time = max(event.timestamp for event in events)
            duration = end_time - start_time
            logger.info(f"   Duration: {duration}ms")
    
    async def run_full_demo(self):
        """运行完整演示"""
        logger.info("🎯 Starting Eko Architecture Integration Demo")
        
        # 初始化
        eko_enabled = await self.initialize()
        
        if not eko_enabled:
            logger.error("❌ Failed to initialize Eko components, aborting demo")
            return
        
        try:
            # 运行演示
            await self.demo_basic_research_flow()
            
            logger.info("\n🎉 Demo completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """主函数"""
    demo = EkoIntegrationDemo()
    await demo.run_full_demo()


if __name__ == "__main__":
    asyncio.run(main()) 