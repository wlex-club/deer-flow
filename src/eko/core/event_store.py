# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""简化的事件存储实现"""

import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


class EventTypes:
    """事件类型常量"""
    RESEARCH_TASK_CREATED = "research.task.created"
    RESEARCH_TASK_UPDATED = "research.task.updated"
    RESEARCH_TASK_COMPLETED = "research.task.completed"
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    SEARCH_COMPLETED = "search.completed"
    CONTENT_PROCESSED = "content.processed"
    REPORT_GENERATED = "report.generated"


@dataclass
class EventMetadata:
    """事件元数据"""
    correlationId: str
    source: str
    userId: Optional[str] = None


@dataclass 
class DeerFlowEvent:
    """DeerFlow事件"""
    id: str
    type: str
    timestamp: int
    payload: Dict[str, Any]
    metadata: EventMetadata


class EventFactory:
    """事件工厂"""
    
    @staticmethod
    def createEvent(event_type: str, payload: Dict[str, Any], metadata: Dict[str, Any]) -> DeerFlowEvent:
        """创建事件"""
        return DeerFlowEvent(
            id=str(uuid.uuid4()),
            type=event_type,
            timestamp=int(time.time() * 1000),
            payload=payload,
            metadata=EventMetadata(
                correlationId=metadata.get("correlationId", "default"),
                source=metadata.get("source", "unknown"),
                userId=metadata.get("userId")
            )
        )


class InMemoryEventStore:
    """内存事件存储"""
    
    def __init__(self):
        self.events: Dict[str, List[DeerFlowEvent]] = {}
    
    def append(self, event: DeerFlowEvent):
        """添加事件"""
        correlation_id = event.metadata.correlationId
        if correlation_id not in self.events:
            self.events[correlation_id] = []
        self.events[correlation_id].append(event)
    
    def getEvents(self, correlation_id: str) -> List[DeerFlowEvent]:
        """获取事件"""
        return self.events.get(correlation_id, [])
    
    def getAllEvents(self) -> List[DeerFlowEvent]:
        """获取所有事件"""
        all_events = []
        for events in self.events.values():
            all_events.extend(events)
        return all_events 