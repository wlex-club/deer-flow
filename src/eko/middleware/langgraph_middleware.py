# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""LangGraph执行中间件，自动捕获和发布事件"""

import asyncio
import logging
from functools import wraps
from typing import Callable, Any, Dict

from ..core.event_bus import EventBus
from ..adapters.langgraph_event_adapter import LangGraphEventAdapter

logger = logging.getLogger(__name__)


class EkoLangGraphMiddleware:
    """LangGraph执行中间件，自动捕获事件"""
    
    def __init__(self, event_bus: EventBus, event_adapter: LangGraphEventAdapter):
        self.event_bus = event_bus
        self.event_adapter = event_adapter
        self.enabled = True
    
    def wrap_node(self, original_node: Callable) -> Callable:
        """包装LangGraph节点以捕获事件"""
        
        @wraps(original_node)
        async def wrapped_node(state: Dict[str, Any], config: Dict[str, Any] = None):
            if not self.enabled:
                return await original_node(state, config)
            
            config = config or {}
            thread_id = config.get("thread_id", "default")
            node_name = getattr(original_node, '__name__', 'unknown')
            
            # 复制旧状态用于比较
            old_state = state.copy() if isinstance(state, dict) else state
            
            try:
                # 发布节点开始事件
                await self._publish_node_start_event(thread_id, node_name, state)
                
                # 执行原始节点
                result = await original_node(state, config)
                
                # 捕获状态变化并发布事件
                if result is not None:
                    events = self.event_adapter.capture_state_change(
                        thread_id, old_state, result, node_name
                    )
                    
                    # 批量发布事件
                    await self._publish_events(events)
                
                # 发布节点完成事件
                await self._publish_node_complete_event(thread_id, node_name, result)
                
                return result
                
            except Exception as e:
                logger.error(f"Error in wrapped node {node_name}: {e}")
                # 发布错误事件
                await self._publish_node_error_event(thread_id, node_name, str(e))
                raise
        
        # 保持原始函数的属性
        wrapped_node.__name__ = getattr(original_node, '__name__', 'wrapped_node')
        wrapped_node.__doc__ = getattr(original_node, '__doc__', '')
        
        return wrapped_node
    
    def wrap_sync_node(self, original_node: Callable) -> Callable:
        """包装同步LangGraph节点"""
        
        @wraps(original_node)
        def wrapped_sync_node(state: Dict[str, Any], config: Dict[str, Any] = None):
            if not self.enabled:
                return original_node(state, config)
            
            config = config or {}
            thread_id = config.get("thread_id", "default")
            node_name = getattr(original_node, '__name__', 'unknown')
            
            # 复制旧状态用于比较
            old_state = state.copy() if isinstance(state, dict) else state
            
            try:
                # 创建异步任务发布开始事件
                asyncio.create_task(
                    self._publish_node_start_event(thread_id, node_name, state)
                )
                
                # 执行原始节点
                result = original_node(state, config)
                
                # 捕获状态变化并发布事件
                if result is not None:
                    events = self.event_adapter.capture_state_change(
                        thread_id, old_state, result, node_name
                    )
                    
                    # 创建异步任务发布事件
                    asyncio.create_task(self._publish_events(events))
                
                # 创建异步任务发布完成事件
                asyncio.create_task(
                    self._publish_node_complete_event(thread_id, node_name, result)
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Error in wrapped sync node {node_name}: {e}")
                # 创建异步任务发布错误事件
                asyncio.create_task(
                    self._publish_node_error_event(thread_id, node_name, str(e))
                )
                raise
        
        # 保持原始函数的属性
        wrapped_sync_node.__name__ = getattr(original_node, '__name__', 'wrapped_sync_node')
        wrapped_sync_node.__doc__ = getattr(original_node, '__doc__', '')
        
        return wrapped_sync_node
    
    async def _publish_node_start_event(self, thread_id: str, node_name: str, state: Any):
        """发布节点开始事件"""
        try:
            from ..core.event_store import EventFactory, EventTypes
            
            payload = {
                "taskId": thread_id,
                "nodeName": node_name,
                "status": "started",
                "timestamp": self._get_timestamp()
            }
            
            event = EventFactory.createEvent(
                EventTypes.AGENT_STARTED,
                payload,
                {
                    "correlationId": thread_id,
                    "source": f"langgraph-middleware-{node_name}"
                }
            )
            
            await self.event_bus.publish(event)
            
        except Exception as e:
            logger.warning(f"Failed to publish node start event: {e}")
    
    async def _publish_node_complete_event(self, thread_id: str, node_name: str, result: Any):
        """发布节点完成事件"""
        try:
            from ..core.event_store import EventFactory, EventTypes
            
            payload = {
                "taskId": thread_id,
                "nodeName": node_name,
                "status": "completed",
                "resultSize": len(str(result)) if result else 0,
                "timestamp": self._get_timestamp()
            }
            
            event = EventFactory.createEvent(
                EventTypes.AGENT_COMPLETED,
                payload,
                {
                    "correlationId": thread_id,
                    "source": f"langgraph-middleware-{node_name}"
                }
            )
            
            await self.event_bus.publish(event)
            
        except Exception as e:
            logger.warning(f"Failed to publish node complete event: {e}")
    
    async def _publish_node_error_event(self, thread_id: str, node_name: str, error: str):
        """发布节点错误事件"""
        try:
            from ..core.event_store import EventFactory, EventTypes
            
            payload = {
                "taskId": thread_id,
                "nodeName": node_name,
                "status": "error",
                "error": error,
                "timestamp": self._get_timestamp()
            }
            
            event = EventFactory.createEvent(
                EventTypes.AGENT_FAILED,
                payload,
                {
                    "correlationId": thread_id,
                    "source": f"langgraph-middleware-{node_name}"
                }
            )
            
            await self.event_bus.publish(event)
            
        except Exception as e:
            logger.warning(f"Failed to publish node error event: {e}")
    
    async def _publish_events(self, events: list):
        """批量发布事件"""
        if not events:
            return
        
        try:
            # 批量发布所有事件
            tasks = [self.event_bus.publish(event) for event in events]
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"Failed to publish events: {e}")
    
    def _get_timestamp(self) -> int:
        """获取当前时间戳"""
        import time
        return int(time.time() * 1000)
    
    def enable(self):
        """启用中间件"""
        self.enabled = True
        logger.info("EkoLangGraphMiddleware enabled")
    
    def disable(self):
        """禁用中间件"""
        self.enabled = False
        logger.info("EkoLangGraphMiddleware disabled")
    
    def is_enabled(self) -> bool:
        """检查中间件是否启用"""
        return self.enabled


class LangGraphTaskTracker:
    """LangGraph任务跟踪器"""
    
    def __init__(self, event_adapter: LangGraphEventAdapter, event_bus: EventBus):
        self.event_adapter = event_adapter
        self.event_bus = event_bus
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def start_task(self, thread_id: str, query: str, user_id: str = None):
        """开始任务跟踪"""
        # 记录任务信息
        self.active_tasks[thread_id] = {
            "query": query,
            "user_id": user_id,
            "start_time": self._get_timestamp(),
            "status": "active"
        }
        
        # 发布任务开始事件
        event = self.event_adapter.create_task_start_event(thread_id, query, user_id)
        await self.event_bus.publish(event)
    
    async def complete_task(self, thread_id: str, final_report: str = None):
        """完成任务跟踪"""
        if thread_id in self.active_tasks:
            task_info = self.active_tasks[thread_id]
            task_info["status"] = "completed"
            task_info["end_time"] = self._get_timestamp()
            task_info["duration"] = task_info["end_time"] - task_info["start_time"]
            
            # 发布任务完成事件
            from ..core.event_store import EventFactory, EventTypes
            
            payload = {
                "taskId": thread_id,
                "finalReport": final_report or "",
                "duration": task_info["duration"],
                "status": "completed",
                "timestamp": task_info["end_time"]
            }
            
            event = EventFactory.createEvent(
                EventTypes.RESEARCH_TASK_COMPLETED,
                payload,
                {
                    "correlationId": thread_id,
                    "source": "langgraph-task-tracker"
                }
            )
            
            await self.event_bus.publish(event)
            
            # 移除活跃任务
            del self.active_tasks[thread_id]
    
    def get_active_tasks(self) -> Dict[str, Dict[str, Any]]:
        """获取活跃任务列表"""
        return self.active_tasks.copy()
    
    def _get_timestamp(self) -> int:
        """获取当前时间戳"""
        import time
 