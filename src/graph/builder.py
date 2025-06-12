# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.prompts.planner_model import StepType

from .types import State
from .nodes import (
    coordinator_node,
    planner_node,
    reporter_node,
    research_team_node,
    researcher_node,
    coder_node,
    human_feedback_node,
    background_investigation_node,
)

logger = logging.getLogger(__name__)

# 尝试导入Eko框架，如果导入失败则使用传统模式
try:
    from src.eko import is_eko_enabled, build_hybrid_graph
    EKO_AVAILABLE = True
    logger.info("✅ Eko framework is available")
except ImportError as e:
    EKO_AVAILABLE = False
    logger.info("⚠️ Eko framework not available, using traditional mode")
    
    def is_eko_enabled():
        return False
    
    def build_hybrid_graph(with_memory=True):
        return None, None


def continue_to_running_research_team(state: State):
    current_plan = state.get("current_plan")
    if not current_plan or not current_plan.steps:
        return "planner"
    if all(step.execution_res for step in current_plan.steps):
        return "planner"
    for step in current_plan.steps:
        if not step.execution_res:
            break
    if step.step_type and step.step_type == StepType.RESEARCH:
        return "researcher"
    if step.step_type and step.step_type == StepType.PROCESSING:
        return "coder"
    return "planner"


def _build_base_graph():
    """Build and return the base state graph with all nodes and edges."""
    builder = StateGraph(State)
    builder.add_edge(START, "coordinator")
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("background_investigator", background_investigation_node)
    builder.add_node("planner", planner_node)
    builder.add_node("reporter", reporter_node)
    builder.add_node("research_team", research_team_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("coder", coder_node)
    builder.add_node("human_feedback", human_feedback_node)
    builder.add_edge("background_investigator", "planner")
    builder.add_conditional_edges(
        "research_team",
        continue_to_running_research_team,
        ["planner", "researcher", "coder"],
    )
    builder.add_edge("reporter", END)
    return builder


def build_graph_with_memory():
    """Build and return the agent workflow graph with memory.
    
    If Eko framework is enabled, returns the Eko-enhanced graph with event tracking.
    Otherwise, returns the traditional graph.
    """
    if EKO_AVAILABLE and is_eko_enabled():
        logger.info("🚀 Building graph with Eko enhancement enabled")
        try:
            graph, eko_components = build_hybrid_graph(with_memory=True)
            if graph is not None:
                logger.info("✅ Successfully built Eko-enhanced graph")
                # 将eko_components附加到graph对象上，以便后续访问
                if hasattr(graph, '_eko_components') or not hasattr(graph, '_eko_components'):
                    graph._eko_components = eko_components
                return graph
            else:
                logger.warning("⚠️ Eko graph construction failed, falling back to traditional mode")
        except Exception as e:
            logger.error(f"❌ Failed to build Eko-enhanced graph: {e}")
            logger.info("🔄 Falling back to traditional graph construction")
    
    # 传统模式构建
    logger.info("🏗️ Building traditional graph with memory")
    memory = MemorySaver()
    builder = _build_base_graph()
    return builder.compile(checkpointer=memory)


def build_graph():
    """Build and return the agent workflow graph without memory.
    
    If Eko framework is enabled, returns the Eko-enhanced graph.
    Otherwise, returns the traditional graph.
    """
    if EKO_AVAILABLE and is_eko_enabled():
        logger.info("🚀 Building graph with Eko enhancement enabled (no memory)")
        try:
            graph, eko_components = build_hybrid_graph(with_memory=False)
            if graph is not None:
                logger.info("✅ Successfully built Eko-enhanced graph (no memory)")
                # 将eko_components附加到graph对象上
                if hasattr(graph, '_eko_components') or not hasattr(graph, '_eko_components'):
                    graph._eko_components = eko_components
                return graph
            else:
                logger.warning("⚠️ Eko graph construction failed, falling back to traditional mode")
        except Exception as e:
            logger.error(f"❌ Failed to build Eko-enhanced graph: {e}")
            logger.info("🔄 Falling back to traditional graph construction")
    
    # 传统模式构建
    logger.info("🏗️ Building traditional graph without memory")
    builder = _build_base_graph()
    return builder.compile()


def get_eko_components(graph):
    """获取图的Eko组件（如果存在）"""
    return getattr(graph, '_eko_components', None)


# 创建默认图实例
graph = build_graph()

# 记录启动时的模式
if EKO_AVAILABLE and is_eko_enabled():
    logger.info("🦌 DeerFlow started with Eko Event-Driven Architecture enabled")
else:
    logger.info("🦌 DeerFlow started in traditional mode")
