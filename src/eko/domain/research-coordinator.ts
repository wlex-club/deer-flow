// Eko架构 - 研究协调器业务逻辑实现

import { EventStore, EventFactory, EventTypes, DeerFlowEvent } from '../core/event-store';
import { EventBus } from '../core/event-bus';

export interface ResearchTask {
  id: string;
  query: string;
  status: 'initiated' | 'planning' | 'executing' | 'completed' | 'failed' | 'cancelled';
  createdAt: number;
  updatedAt: number;
  assignedAgents: string[];
  results?: any;
}

export interface Agent {
  id: string;
  type: AgentType;
  status: 'idle' | 'busy' | 'failed';
  capabilities: string[];
}

export type AgentType = 'researcher' | 'analyzer' | 'writer' | 'coder' | 'presenter';

export class ResearchCoordinator {
  constructor(
    private eventStore: EventStore,
    private eventBus: EventBus
  ) {
    this.subscribeToEvents();
  }

  async startResearch(query: string, userId?: string): Promise<ResearchTask> {
    const taskId = this.generateTaskId();
    const task: ResearchTask = {
      id: taskId,
      query,
      status: 'initiated',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      assignedAgents: []
    };

    // 验证任务
    await this.validateTask(task);

    // 创建任务创建事件
    const event = EventFactory.createEvent(
      EventTypes.RESEARCH_TASK_CREATED,
      { 
        taskId: task.id,
        query: task.query,
        status: task.status,
        createdAt: task.createdAt
      },
      { 
        correlationId: taskId,
        source: 'research-coordinator',
        userId 
      }
    );

    // 存储事件
    await this.eventStore.append([event]);
    
    // 发布事件到事件总线
    await this.eventBus.publish(event);

    return task;
  }

  async assignAgent(taskId: string, agentType: AgentType): Promise<void> {
    const agent = await this.createAgent(agentType);
    
    const event = EventFactory.createEvent(
      EventTypes.AGENT_ASSIGNED,
      {
        taskId,
        agentId: agent.id,
        agentType: agent.type,
        assignedAt: Date.now()
      },
      {
        correlationId: taskId,
        source: 'research-coordinator'
      }
    );

    await this.eventStore.append([event]);
    await this.eventBus.publish(event);
  }

  async updateTaskStatus(taskId: string, status: ResearchTask['status'], results?: any): Promise<void> {
    const event = EventFactory.createEvent(
      EventTypes.RESEARCH_TASK_UPDATED,
      {
        taskId,
        status,
        updatedAt: Date.now(),
        results
      },
      {
        correlationId: taskId,
        source: 'research-coordinator'
      }
    );

    await this.eventStore.append([event]);
    await this.eventBus.publish(event);
  }

  async completeTask(taskId: string, results: any): Promise<void> {
    const event = EventFactory.createEvent(
      EventTypes.RESEARCH_TASK_COMPLETED,
      {
        taskId,
        results,
        completedAt: Date.now()
      },
      {
        correlationId: taskId,
        source: 'research-coordinator'
      }
    );

    await this.eventStore.append([event]);
    await this.eventBus.publish(event);
  }

  async cancelTask(taskId: string, reason: string): Promise<void> {
    const event = EventFactory.createEvent(
      EventTypes.RESEARCH_TASK_CANCELLED,
      {
        taskId,
        reason,
        cancelledAt: Date.now()
      },
      {
        correlationId: taskId,
        source: 'research-coordinator'
      }
    );

    await this.eventStore.append([event]);
    await this.eventBus.publish(event);
  }

  private async validateTask(task: ResearchTask): Promise<void> {
    if (!task.query || task.query.trim().length === 0) {
      throw new Error('Research query cannot be empty');
    }

    if (task.query.length > 1000) {
      throw new Error('Research query is too long (max 1000 characters)');
    }

    // 可以添加更多验证逻辑
  }

  private async createAgent(agentType: AgentType): Promise<Agent> {
    const agentCapabilities = this.getAgentCapabilities(agentType);
    
    return {
      id: this.generateAgentId(),
      type: agentType,
      status: 'idle',
      capabilities: agentCapabilities
    };
  }

  private getAgentCapabilities(agentType: AgentType): string[] {
    const capabilityMap: Record<AgentType, string[]> = {
      researcher: ['web-search', 'content-analysis', 'fact-checking'],
      analyzer: ['data-processing', 'pattern-recognition', 'summarization'],
      writer: ['content-generation', 'report-writing', 'editing'],
      coder: ['code-generation', 'technical-analysis', 'debugging'],
      presenter: ['slide-creation', 'visualization', 'storytelling']
    };

    return capabilityMap[agentType] || [];
  }

  private subscribeToEvents(): void {
    // 订阅智能体完成事件
    this.eventBus.subscribe(EventTypes.AGENT_COMPLETED, async (event) => {
      await this.handleAgentCompleted(event);
    });

    // 订阅智能体失败事件
    this.eventBus.subscribe(EventTypes.AGENT_FAILED, async (event) => {
      await this.handleAgentFailed(event);
    });
  }

  private async handleAgentCompleted(event: DeerFlowEvent): Promise<void> {
    const { taskId, agentId } = event.payload;
    console.log(`Agent ${agentId} completed work on task ${taskId}`);
    await this.checkTaskCompletion(taskId);
  }

  private async handleAgentFailed(event: DeerFlowEvent): Promise<void> {
    const { taskId, agentId, error } = event.payload;
    console.error(`Agent ${agentId} failed on task ${taskId}:`, error);
    await this.handleTaskFailure(taskId, error);
  }

  private async checkTaskCompletion(taskId: string): Promise<void> {
    const taskEvents = await this.eventStore.getEvents(taskId);
    const task = this.reconstructTaskFromEvents(taskEvents);
    
    if (this.isTaskComplete(task)) {
      const event = EventFactory.createEvent(
        EventTypes.RESEARCH_TASK_COMPLETED,
        { taskId, results: task.results, completedAt: Date.now() },
        { correlationId: taskId, source: 'research-coordinator' }
      );
      
      await this.eventStore.append([event]);
      await this.eventBus.publish(event);
    }
  }

  private async handleTaskFailure(taskId: string, error: string): Promise<void> {
    const event = EventFactory.createEvent(
      EventTypes.RESEARCH_TASK_UPDATED,
      { taskId, status: 'failed', error, updatedAt: Date.now() },
      { correlationId: taskId, source: 'research-coordinator' }
    );

    await this.eventStore.append([event]);
    await this.eventBus.publish(event);
  }

  private reconstructTaskFromEvents(events: DeerFlowEvent[]): ResearchTask {
    let task: Partial<ResearchTask> = {};
    
    for (const event of events) {
      switch (event.type) {
        case EventTypes.RESEARCH_TASK_CREATED:
          task = {
            id: event.payload.taskId,
            query: event.payload.query,
            status: event.payload.status,
            createdAt: event.payload.createdAt,
            updatedAt: event.payload.createdAt,
            assignedAgents: []
          };
          break;
          
        case EventTypes.AGENT_ASSIGNED:
          if (task.assignedAgents) {
            task.assignedAgents.push(event.payload.agentId);
          }
          break;
          
        case EventTypes.RESEARCH_TASK_UPDATED:
          task.status = event.payload.status;
          task.updatedAt = event.payload.updatedAt;
          if (event.payload.results) {
            task.results = event.payload.results;
          }
          break;
      }
    }
    
    return task as ResearchTask;
  }

  private isTaskComplete(task: ResearchTask): boolean {
    return task.assignedAgents.length > 0 && task.results !== undefined;
  }

  private generateTaskId(): string {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateAgentId(): string {
    return `agent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
} 