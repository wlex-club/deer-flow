# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""混合模式的LangGraph构建器，同时支持LangGraph和Eko架构"""

import logging
from typing import Tuple, Optional

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from ..middleware.langgraph_middleware import EkoLangGraphMiddleware, LangGraphTaskTracker
from ..adapters.langgraph_event_adapter import LangGraphEventAdapter
from ..core.event_bus import EventBusFactory
from ..core.event_store import InMemoryEventStore
from ..config import get_eko_config

# 导入原有的类型和节点
from src.graph.types import State
from src.graph.nodes import (
    coordinator_node,
    planner_node,
    reporter_node,
    research_team_node,
    researcher_node,
    coder_node,
    human_feedback_node,
    background_investigation_node,
)
from src.graph.builder import continue_to_running_research_team

logger = logging.getLogger(__name__)


def build_hybrid_graph(with_memory: bool = True):
    """构建混合模式的图，同时支持LangGraph和Eko架构"""
    
    config = get_eko_config()
    
    # 初始化Eko组件
    event_store = None
    event_bus = None
    middleware = None
    task_tracker = None
    
    if config.enabled:
        try:
            # 创建事件存储和事件总线
            event_store = InMemoryEventStore()
            event_bus = EventBusFactory.create()
            
            # 创建事件适配器和中间件
            event_adapter = LangGraphEventAdapter()
            middleware = EkoLangGraphMiddleware(event_bus, event_adapter)
            task_tracker = LangGraphTaskTracker(event_adapter, event_bus)
            
            logger.info("Eko components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Eko components: {e}")
            config.enabled = False
    
    # 构建状态图
    builder = StateGraph(State)
    builder.add_edge(START, "coordinator")
    
    # 添加节点（根据配置决定是否包装）
    if config.enabled and middleware:
        # 使用Eko中间件包装节点
        builder.add_node("coordinator", middleware.wrap_sync_node(coordinator_node))
        builder.add_node("background_investigator", middleware.wrap_sync_node(background_investigation_node))
        builder.add_node("planner", middleware.wrap_sync_node(planner_node))
        builder.add_node("reporter", middleware.wrap_sync_node(reporter_node))
        builder.add_node("research_team", middleware.wrap_sync_node(research_team_node))
        builder.add_node("researcher", middleware.wrap_node(researcher_node))
        builder.add_node("coder", middleware.wrap_node(coder_node))
        builder.add_node("human_feedback", middleware.wrap_sync_node(human_feedback_node))
    else:
        # 使用原始节点
        builder.add_node("coordinator", coordinator_node)
        builder.add_node("background_investigator", background_investigation_node)
        builder.add_node("planner", planner_node)
        builder.add_node("reporter", reporter_node)
        builder.add_node("research_team", research_team_node)
        builder.add_node("researcher", researcher_node)
        builder.add_node("coder", coder_node)
        builder.add_node("human_feedback", human_feedback_node)
    
    # 添加边和条件边
    builder.add_edge("background_investigator", "planner")
    builder.add_conditional_edges(
        "research_team",
        continue_to_running_research_team,
        ["planner", "researcher", "coder"],
    )
    builder.add_edge("reporter", END)
    
    # 编译图
    if with_memory:
        memory = MemorySaver()
        compiled_graph = builder.compile(checkpointer=memory)
    else:
        compiled_graph = builder.compile()
    
    # 返回图和Eko组件
    eko_components = {
        "event_store": event_store,
        "event_bus": event_bus,
        "middleware": middleware,
        "task_tracker": task_tracker,
        "config": config
    } if config.enabled else None
    
    return compiled_graph, eko_components 