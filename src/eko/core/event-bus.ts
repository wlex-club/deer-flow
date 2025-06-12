// Eko架构 - 事件总线实现

import { DeerFlowEvent, EventType } from './event-store';

export type EventHandler = (event: DeerFlowEvent) => Promise<void>;

export interface EventBus {
  subscribe(eventType: EventType, handler: EventHandler): void;
  unsubscribe(eventType: EventType, handler: EventHandler): void;
  publish(event: DeerFlowEvent): Promise<void>;
  publishBatch(events: DeerFlowEvent[]): Promise<void>;
}

export class InMemoryEventBus implements EventBus {
  private handlers: Map<EventType, Set<EventHandler>> = new Map();
  private middlewares: EventMiddleware[] = [];

  subscribe(eventType: EventType, handler: EventHandler): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }
    this.handlers.get(eventType)!.add(handler);
  }

  unsubscribe(eventType: EventType, handler: EventHandler): void {
    const handlersSet = this.handlers.get(eventType);
    if (handlersSet) {
      handlersSet.delete(handler);
      if (handlersSet.size === 0) {
        this.handlers.delete(eventType);
      }
    }
  }

  async publish(event: DeerFlowEvent): Promise<void> {
    // 应用中间件
    let processedEvent = event;
    for (const middleware of this.middlewares) {
      processedEvent = await middleware.process(processedEvent);
    }

    const handlers = this.handlers.get(event.type as EventType);
    if (handlers) {
      // 并发执行所有处理器
      const promises = Array.from(handlers).map(handler => 
        this.executeHandler(handler, processedEvent)
      );
      await Promise.allSettled(promises);
    }
  }

  async publishBatch(events: DeerFlowEvent[]): Promise<void> {
    const promises = events.map(event => this.publish(event));
    await Promise.allSettled(promises);
  }

  addMiddleware(middleware: EventMiddleware): void {
    this.middlewares.push(middleware);
  }

  private async executeHandler(handler: EventHandler, event: DeerFlowEvent): Promise<void> {
    try {
      await handler(event);
    } catch (error) {
      console.error(`Error handling event ${event.type}:`, error);
      // 这里可以添加错误重试逻辑或死信队列
    }
  }
}

// 事件中间件接口
export interface EventMiddleware {
  process(event: DeerFlowEvent): Promise<DeerFlowEvent>;
}

// 日志中间件
export class LoggingMiddleware implements EventMiddleware {
  async process(event: DeerFlowEvent): Promise<DeerFlowEvent> {
    console.log(`[EventBus] Processing event: ${event.type}`, {
      id: event.id,
      timestamp: event.timestamp,
      correlationId: event.metadata.correlationId
    });
    return event;
  }
}

// 性能监控中间件
export class PerformanceMiddleware implements EventMiddleware {
  private metrics: Map<string, { count: number; avgTime: number }> = new Map();

  async process(event: DeerFlowEvent): Promise<DeerFlowEvent> {
    const startTime = performance.now();
    
    // 处理完成后记录性能指标
    setTimeout(() => {
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      this.updateMetrics(event.type, duration);
    }, 0);

    return event;
  }

  private updateMetrics(eventType: string, duration: number): void {
    const current = this.metrics.get(eventType) || { count: 0, avgTime: 0 };
    const newCount = current.count + 1;
    const newAvgTime = (current.avgTime * current.count + duration) / newCount;
    
    this.metrics.set(eventType, { count: newCount, avgTime: newAvgTime });
  }

  getMetrics(): Map<string, { count: number; avgTime: number }> {
    return new Map(this.metrics);
  }
}

// 事件过滤中间件
export class FilterMiddleware implements EventMiddleware {
  constructor(private filterFn: (event: DeerFlowEvent) => boolean) {}

  async process(event: DeerFlowEvent): Promise<DeerFlowEvent> {
    if (!this.filterFn(event)) {
      throw new Error(`Event ${event.type} filtered out`);
    }
    return event;
  }
}

// 事件总线工厂
export class EventBusFactory {
  static create(): EventBus {
    const eventBus = new InMemoryEventBus();
    
    // 添加默认中间件
    eventBus.addMiddleware(new LoggingMiddleware());
    eventBus.addMiddleware(new PerformanceMiddleware());
    
    return eventBus;
  }

  static createWithMiddlewares(middlewares: EventMiddleware[]): EventBus {
    const eventBus = new InMemoryEventBus();
    
    middlewares.forEach(middleware => {
      eventBus.addMiddleware(middleware);
    });
    
    return eventBus;
  }
} 