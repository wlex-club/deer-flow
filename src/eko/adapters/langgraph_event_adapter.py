# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""LangGraph到Eko架构的事件适配器"""

import json
import logging
from typing import Dict, Any, List, Optional
from langgraph.graph import MessagesState

from ..core.event_store import DeerFlowEvent, EventFactory, EventTypes

logger = logging.getLogger(__name__)


class LangGraphEventAdapter:
    """LangGraph状态到事件的适配器"""
    
    def __init__(self):
        self.state_snapshots: Dict[str, MessagesState] = {}
    
    def capture_state_change(self, 
                           thread_id: str, 
                           old_state: MessagesState, 
                           new_state: MessagesState,
                           node_name: str) -> List[DeerFlowEvent]:
        """捕获状态变化并转换为事件"""
        events = []
        
        try:
            # 检测计划变化
            if self._has_plan_changed(old_state, new_state):
                plan_event = self._create_plan_event(thread_id, new_state, node_name)
                if plan_event:
                    events.append(plan_event)
            
            # 检测消息变化
            if self._has_messages_changed(old_state, new_state):
                message_event = self._create_message_event(thread_id, new_state, node_name)
                if message_event:
                    events.append(message_event)
            
            # 检测智能体状态变化
            if node_name in ['researcher', 'coder', 'planner', 'reporter']:
                agent_event = self._create_agent_event(thread_id, new_state, node_name)
                if agent_event:
                    events.append(agent_event)
            
            # 检测资源变化
            if self._has_resources_changed(old_state, new_state):
                resource_event = self._create_resource_event(thread_id, new_state, node_name)
                if resource_event:
                    events.append(resource_event)
                    
        except Exception as e:
            logger.error(f"Error capturing state change for thread {thread_id}: {e}")
        
        return events
    
    def _has_plan_changed(self, old_state: MessagesState, new_state: MessagesState) -> bool:
        """检测计划是否发生变化"""
        old_plan = old_state.get("current_plan")
        new_plan = new_state.get("current_plan")
        return old_plan != new_plan
    
    def _has_messages_changed(self, old_state: MessagesState, new_state: MessagesState) -> bool:
        """检测消息是否发生变化"""
        old_messages = old_state.get("messages", [])
        new_messages = new_state.get("messages", [])
        return len(old_messages) != len(new_messages)
    
    def _has_resources_changed(self, old_state: MessagesState, new_state: MessagesState) -> bool:
        """检测资源是否发生变化"""
        old_resources = old_state.get("resources", [])
        new_resources = new_state.get("resources", [])
        return len(old_resources) != len(new_resources)
    
    def _create_plan_event(self, thread_id: str, state: MessagesState, node_name: str) -> Optional[DeerFlowEvent]:
        """创建计划相关事件"""
        current_plan = state.get("current_plan")
        if not current_plan:
            return None
        
        payload = {
            "taskId": thread_id,
            "planContent": str(current_plan),
            "status": "planning",
            "nodeSource": node_name,
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.RESEARCH_TASK_UPDATED,
            payload,
            {
                "correlationId": thread_id,
                "source": f"langgraph-{node_name}"
            }
        )
    
    def _create_message_event(self, thread_id: str, state: MessagesState, node_name: str) -> Optional[DeerFlowEvent]:
        """创建消息相关事件"""
        messages = state.get("messages", [])
        if not messages:
            return None
        
        latest_message = messages[-1]
        
        payload = {
            "taskId": thread_id,
            "messageContent": str(latest_message),
            "nodeSource": node_name,
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.CONTENT_PROCESSED,
            payload,
            {
                "correlationId": thread_id,
                "source": f"langgraph-{node_name}"
            }
        )
    
    def _create_agent_event(self, thread_id: str, state: MessagesState, node_name: str) -> Optional[DeerFlowEvent]:
        """创建智能体相关事件"""
        payload = {
            "taskId": thread_id,
            "agentId": f"{node_name}_{thread_id}",
            "agentType": node_name,
            "status": "started",
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.AGENT_STARTED,
            payload,
            {
                "correlationId": thread_id,
                "source": f"langgraph-{node_name}"
            }
        )
    
    def _create_resource_event(self, thread_id: str, state: MessagesState, node_name: str) -> Optional[DeerFlowEvent]:
        """创建资源相关事件"""
        resources = state.get("resources", [])
        if not resources:
            return None
        
        payload = {
            "taskId": thread_id,
            "resources": [self._serialize_resource(r) for r in resources],
            "resourceCount": len(resources),
            "nodeSource": node_name,
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.CONTENT_PROCESSED,
            payload,
            {
                "correlationId": thread_id,
                "source": f"langgraph-{node_name}",
                "causationId": f"{thread_id}-{node_name}"
            }
        )
    
    def _serialize_plan(self, plan: Any) -> Dict[str, Any]:
        """序列化计划对象"""
        try:
            if hasattr(plan, 'model_dump'):
                return plan.model_dump()
            elif hasattr(plan, '__dict__'):
                return plan.__dict__
            else:
                return {"content": str(plan)}
        except Exception as e:
            logger.warning(f"Failed to serialize plan: {e}")
            return {"content": str(plan)}
    
    def _serialize_resource(self, resource: Any) -> Dict[str, Any]:
        """序列化资源对象"""
        try:
            if hasattr(resource, 'model_dump'):
                return resource.model_dump()
            elif hasattr(resource, '__dict__'):
                return resource.__dict__
            else:
                return {"content": str(resource)}
        except Exception as e:
            logger.warning(f"Failed to serialize resource: {e}")
            return {"content": str(resource)}
    
    def _get_timestamp(self) -> int:
        """获取当前时间戳"""
        import time
        return int(time.time() * 1000)
    
    def create_task_start_event(self, thread_id: str, query: str, user_id: Optional[str] = None) -> DeerFlowEvent:
        """创建任务开始事件"""
        payload = {
            "taskId": thread_id,
            "query": query,
            "status": "initiated",
            "userId": user_id,
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.RESEARCH_TASK_CREATED,
            payload,
            {
                "correlationId": thread_id,
                "source": "langgraph-adapter",
                "userId": user_id
            }
        )
    
    def create_task_complete_event(self, thread_id: str, final_report: str) -> DeerFlowEvent:
        """创建任务完成事件"""
        payload = {
            "taskId": thread_id,
            "finalReport": final_report,
            "status": "completed",
            "timestamp": self._get_timestamp()
        }
        
        return EventFactory.createEvent(
            EventTypes.RESEARCH_TASK_COMPLETED,
            payload,
            {
                "correlationId": thread_id,
                "source": "langgraph-adapter"
            }
        ) 