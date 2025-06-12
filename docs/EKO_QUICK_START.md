# Eko架构快速集成指南

## 🚀 快速开始

### 1. 环境配置

```bash
# 设置环境变量启用Eko架构
export EKO_ENABLED=true
export EKO_DEBUG=true
export EKO_LANGGRAPH_COMPAT=true
```

### 2. 基础集成

```python
# 使用Eko增强的图构建器
from src.eko.graph.hybrid_builder import build_hybrid_graph

# 构建混合模式的图
graph, eko_components = build_hybrid_graph(with_memory=True)

if eko_components:
    event_store = eko_components["event_store"]
    event_bus = eko_components["event_bus"]
    task_tracker = eko_components["task_tracker"]
    
    print("✅ Eko架构已启用")
else:
    print("⚠️ 运行在传统LangGraph模式")
```

### 3. 事件监听

```python
async def setup_event_monitoring(event_bus):
    """设置事件监听"""
    
    async def log_event(event):
        print(f"📝 Event: {event.type}")
        print(f"   Task: {event.metadata.correlationId}")
        print(f"   Data: {event.payload}")
    
    # 订阅关键事件
    from src.eko.core.event_store import EventTypes
    
    event_bus.subscribe(EventTypes.RESEARCH_TASK_CREATED, log_event)
    event_bus.subscribe(EventTypes.AGENT_STARTED, log_event)
    event_bus.subscribe(EventTypes.AGENT_COMPLETED, log_event)
```

### 4. 任务执行

```python
async def run_research_task():
    """运行研究任务"""
    
    # 构建输入
    input_data = {
        "messages": [{"role": "user", "content": "研究AI最新趋势"}],
        "auto_accepted_plan": True,
        "enable_background_investigation": True,
    }
    
    thread_id = "research_001"
    
    # 开始任务跟踪
    if task_tracker:
        await task_tracker.start_task(thread_id, "研究AI最新趋势")
    
    # 执行图
    async for chunk in graph.astream(
        input_data,
        config={"thread_id": thread_id}
    ):
        print(f"📊 Progress: {list(chunk.keys())}")
    
    # 完成任务
    if task_tracker:
        await task_tracker.complete_task(thread_id)
```

### 5. 运行测试

```bash
# 运行集成测试
python scripts/test_eko_integration.py
```

## 🔧 配置选项

### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `EKO_ENABLED` | `true` | 是否启用Eko架构 |
| `EKO_DEBUG` | `false` | 调试模式 |
| `EKO_EVENT_STORE` | `memory` | 事件存储类型 |
| `EKO_EVENT_BUS` | `memory` | 事件总线类型 |
| `EKO_BATCH_SIZE` | `100` | 批处理大小 |

### 代码配置

```python
from src.eko.config import EkoConfig

config = EkoConfig(
    enabled=True,
    debug_mode=True,
    batch_size=50,
    event_store_type="memory",
    event_bus_type="memory"
)
```

## 📊 监控和调试

### 查看事件历史

```python
# 获取指定任务的事件
events = event_store.getEvents("task_id")

for event in events:
    print(f"Event: {event.type} at {event.timestamp}")
    print(f"Data: {event.payload}")
```

### 性能指标

```python
# 获取活跃任务
active_tasks = task_tracker.get_active_tasks()
print(f"Active tasks: {len(active_tasks)}")

# 事件统计
total_events = len(event_store.events)
print(f"Total events: {total_events}")
```

## 🚨 故障排除

### 常见问题

1. **Eko组件初始化失败**
   ```python
   # 检查配置
   from src.eko.config import get_eko_config
   config = get_eko_config()
   print(f"Eko enabled: {config.enabled}")
   ```

2. **事件未被捕获**
   ```python
   # 检查中间件状态
   if middleware:
       print(f"Middleware enabled: {middleware.is_enabled()}")
   ```

3. **性能问题**
   ```bash
   # 减少批处理大小
   export EKO_BATCH_SIZE=50
   export EKO_FLUSH_INTERVAL=500
   ```

### 禁用Eko架构

```bash
# 临时禁用
export EKO_ENABLED=false

# 或在代码中
os.environ["EKO_ENABLED"] = "false"
```

## 📈 进阶用法

### 自定义事件处理器

```python
class CustomEventHandler:
    async def handle_task_created(self, event):
        """处理任务创建事件"""
        task_id = event.payload["taskId"]
        print(f"New task created: {task_id}")
    
    async def handle_agent_completed(self, event):
        """处理智能体完成事件"""
        agent_type = event.payload["agentType"]
        print(f"Agent {agent_type} completed")

# 注册处理器
handler = CustomEventHandler()
event_bus.subscribe(EventTypes.RESEARCH_TASK_CREATED, handler.handle_task_created)
event_bus.subscribe(EventTypes.AGENT_COMPLETED, handler.handle_agent_completed)
```

### 事件重放

```python
async def replay_task_events(task_id):
    """重放指定任务的事件"""
    events = event_store.getEvents(task_id)
    
    for event in sorted(events, key=lambda e: e.timestamp):
        print(f"Replaying: {event.type} at {event.timestamp}")
        # 可以在这里重新处理事件
```

## 🎯 最佳实践

1. **渐进式集成**: 先在测试环境启用，验证稳定性
2. **监控事件量**: 注意事件数量对内存的影响
3. **合理配置**: 根据系统负载调整批处理参数
4. **错误处理**: 确保事件处理失败不影响主流程
5. **定期清理**: 在生产环境中定期清理历史事件

## 📚 相关文档

- [Eko架构专家级集成方案](./EKO_EXPERT_INTEGRATION_PLAN.md)
- [原始Eko架构集成指南](./EKO_ARCHITECTURE_INTEGRATION.md)
- [LangGraph官方文档](https://python.langchain.com/docs/langgraph) 