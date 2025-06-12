// Eko架构 - 事件存储核心实现

export interface DeerFlowEvent {
  id: string;
  timestamp: number;
  type: string;
  payload: any;
  metadata: EventMetadata;
  version: number;
}

export interface EventMetadata {
  correlationId: string;
  causationId?: string;
  version: number;
  source: string;
  userId?: string;
}

export interface EventStore {
  append(events: DeerFlowEvent[]): Promise<void>;
  getEvents(streamId: string, fromVersion?: number): Promise<DeerFlowEvent[]>;
  getEventsByType(eventType: string): Promise<DeerFlowEvent[]>;
  getUnpublishedEvents(): Promise<DeerFlowEvent[]>;
  markAsPublished(eventId: string): Promise<void>;
}

// 内存版本事件存储 (生产环境可替换为数据库实现)
export class InMemoryEventStore implements EventStore {
  private events: Map<string, DeerFlowEvent[]> = new Map();
  private unpublishedEvents: Set<string> = new Set();
  private allEvents: DeerFlowEvent[] = [];

  async append(events: DeerFlowEvent[]): Promise<void> {
    for (const event of events) {
      // 添加到全局事件列表
      this.allEvents.push(event);
      
      // 按流ID组织事件
      const streamId = this.extractStreamId(event);
      if (!this.events.has(streamId)) {
        this.events.set(streamId, []);
      }
      this.events.get(streamId)!.push(event);
      
      // 标记为未发布
      this.unpublishedEvents.add(event.id);
    }
  }

  async getEvents(streamId: string, fromVersion?: number): Promise<DeerFlowEvent[]> {
    const streamEvents = this.events.get(streamId) || [];
    if (fromVersion !== undefined) {
      return streamEvents.filter(e => e.version >= fromVersion);
    }
    return streamEvents;
  }

  async getEventsByType(eventType: string): Promise<DeerFlowEvent[]> {
    return this.allEvents.filter(e => e.type === eventType);
  }

  async getUnpublishedEvents(): Promise<DeerFlowEvent[]> {
    return this.allEvents.filter(e => this.unpublishedEvents.has(e.id));
  }

  async markAsPublished(eventId: string): Promise<void> {
    this.unpublishedEvents.delete(eventId);
  }

  private extractStreamId(event: DeerFlowEvent): string {
    // 从事件中提取流ID，通常是聚合根ID
    return event.payload.taskId || event.payload.id || 'default';
  }
}

// 事件工厂
export class EventFactory {
  static createEvent(
    type: string,
    payload: any,
    metadata: Partial<EventMetadata> = {}
  ): DeerFlowEvent {
    return {
      id: this.generateId(),
      timestamp: Date.now(),
      type,
      payload,
      version: 1,
      metadata: {
        correlationId: metadata.correlationId || this.generateId(),
        causationId: metadata.causationId,
        version: metadata.version || 1,
        source: metadata.source || 'deer-flow',
        userId: metadata.userId
      }
    };
  }

  private static generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }
}

// 事件类型定义
export const EventTypes = {
  // 研究任务事件
  RESEARCH_TASK_CREATED: 'research.task.created',
  RESEARCH_TASK_UPDATED: 'research.task.updated',
  RESEARCH_TASK_COMPLETED: 'research.task.completed',
  RESEARCH_TASK_CANCELLED: 'research.task.cancelled',
  
  // 智能体事件
  AGENT_ASSIGNED: 'agent.assigned',
  AGENT_STARTED: 'agent.started',
  AGENT_COMPLETED: 'agent.completed',
  AGENT_FAILED: 'agent.failed',
  
  // 搜索事件
  SEARCH_INITIATED: 'search.initiated',
  SEARCH_COMPLETED: 'search.completed',
  SEARCH_FAILED: 'search.failed',
  
  // 内容处理事件
  CONTENT_PROCESSED: 'content.processed',
  CONTENT_VALIDATED: 'content.validated',
  
  // 输出生成事件
  REPORT_GENERATED: 'report.generated',
  PPT_CREATED: 'ppt.created',
  PODCAST_GENERATED: 'podcast.generated'
} as const;

export type EventType = typeof EventTypes[keyof typeof EventTypes]; 