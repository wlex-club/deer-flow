# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""简化的事件总线实现"""

import asyncio
import logging
from typing import Dict, List, Callable, Any
from .event_store import DeerFlowEvent

logger = logging.getLogger(__name__)


class EventBus:
    """简化的事件总线"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        """订阅事件"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """取消订阅"""
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(handler)
            except ValueError:
                pass
    
    async def publish(self, event: DeerFlowEvent):
        """发布事件"""
        handlers = self.subscribers.get(event.type, [])
        
        if handlers:
            # 并行执行所有处理器
            tasks = []
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        tasks.append(handler(event))
                    else:
                        # 同步函数包装为异步
                        tasks.append(asyncio.create_task(
                            asyncio.to_thread(handler, event)
                        ))
                except Exception as e:
                    logger.error(f"Error creating task for handler: {e}")
            
            if tasks:
                # 等待所有任务完成，忽略异常
                await asyncio.gather(*tasks, return_exceptions=True)


class EventBusFactory:
    """事件总线工厂"""
    
    @staticmethod
    def create(bus_type: str = "memory") -> EventBus:
        """创建事件总线"""
        if bus_type == "memory":
            return EventBus()
        else:
            logger.warning(f"Unsupported bus type: {bus_type}, using memory bus")
            return EventBus() 