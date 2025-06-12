# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""Eko架构配置管理"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class EkoConfig:
    """Eko架构配置"""
    
    # 基础设置
    enabled: bool = True
    event_store_type: str = "memory"  # memory, redis, postgres
    event_bus_type: str = "memory"   # memory, redis, kafka
    langgraph_compat: bool = True
    debug_mode: bool = False
    
    # 性能设置
    batch_size: int = 100
    flush_interval: int = 1000  # ms
    max_events_per_batch: int = 500
    
    # 持久化设置
    persistence_enabled: bool = False
    snapshot_interval: int = 1000  # events
    
    # 监控设置
    metrics_enabled: bool = True
    health_check_interval: int = 30  # seconds
    
    # 错误处理
    max_retry_attempts: int = 3
    retry_delay: int = 1000  # ms


def get_eko_config() -> EkoConfig:
    """获取Eko配置"""
    return EkoConfig(
        enabled=_get_bool_env("EKO_ENABLED", True),
        event_store_type=os.getenv("EKO_EVENT_STORE", "memory"),
        event_bus_type=os.getenv("EKO_EVENT_BUS", "memory"),
        langgraph_compat=_get_bool_env("EKO_LANGGRAPH_COMPAT", True),
        debug_mode=_get_bool_env("EKO_DEBUG", False),
        
        batch_size=_get_int_env("EKO_BATCH_SIZE", 100),
        flush_interval=_get_int_env("EKO_FLUSH_INTERVAL", 1000),
        max_events_per_batch=_get_int_env("EKO_MAX_EVENTS_PER_BATCH", 500),
        
        persistence_enabled=_get_bool_env("EKO_PERSISTENCE_ENABLED", False),
        snapshot_interval=_get_int_env("EKO_SNAPSHOT_INTERVAL", 1000),
        
        metrics_enabled=_get_bool_env("EKO_METRICS_ENABLED", True),
        health_check_interval=_get_int_env("EKO_HEALTH_CHECK_INTERVAL", 30),
        
        max_retry_attempts=_get_int_env("EKO_MAX_RETRY_ATTEMPTS", 3),
        retry_delay=_get_int_env("EKO_RETRY_DELAY", 1000),
    )


def _get_bool_env(key: str, default: bool) -> bool:
    """从环境变量获取布尔值"""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def _get_int_env(key: str, default: int) -> int:
    """从环境变量获取整数值"""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def is_eko_enabled() -> bool:
    """检查Eko是否启用"""
    return get_eko_config().enabled


def is_debug_mode() -> bool:
    """检查是否为调试模式"""
    return get_eko_config().debug_mode 