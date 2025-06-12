// Eko架构演示用例 - 展示事件驱动的研究流程

import { InMemoryEventStore, EventFactory, EventTypes } from './core/event-store';
import { EventBusFactory } from './core/event-bus';
import { ResearchCoordinator } from './domain/research-coordinator';

async function runEkoArchitectureDemo() {
  console.log('🚀 启动 DeerFlow Eko架构演示');
  console.log('=====================================');

  // 1. 初始化核心组件
  const eventStore = new InMemoryEventStore();
  const eventBus = EventBusFactory.create();
  const coordinator = new ResearchCoordinator(eventStore, eventBus);

  // 2. 模拟用户启动研究任务
  console.log('\n📋 步骤1: 创建研究任务');
  const task = await coordinator.startResearch(
    'AI在医疗领域的应用现状与未来发展趋势',
    'user_123'
  );
  console.log(`✅ 任务已创建: ${task.id}`);
  console.log(`   查询: ${task.query}`);
  console.log(`   状态: ${task.status}`);

  // 3. 分配智能体
  console.log('\n🤖 步骤2: 分配智能体');
  await coordinator.assignAgent(task.id, 'researcher');
  await coordinator.assignAgent(task.id, 'analyzer');
  await coordinator.assignAgent(task.id, 'writer');
  console.log('✅ 智能体分配完成');

  // 4. 模拟智能体工作完成
  console.log('\n⚡ 步骤3: 模拟智能体工作流程');
  
  // 模拟研究智能体完成搜索
  const searchCompletedEvent = EventFactory.createEvent(
    EventTypes.SEARCH_COMPLETED,
    {
      taskId: task.id,
      agentId: 'agent_researcher_001',
      results: {
        sources: [
          'https://example.com/ai-healthcare-2024',
          'https://medical-journal.com/ai-trends'
        ],
        keyFindings: [
          'AI诊断准确率提升30%',
          '远程医疗采用率增长200%',
          '药物研发周期缩短40%'
        ]
      }
    },
    { correlationId: task.id, source: 'research-agent' }
  );

  await eventStore.append([searchCompletedEvent]);
  await eventBus.publish(searchCompletedEvent);
  console.log('✅ 搜索智能体完成工作');

  // 5. 查看事件历史
  console.log('\n📚 步骤4: 查看事件历史');
  const allTaskEvents = await eventStore.getEvents(task.id);
  console.log(`✅ 任务 ${task.id} 共产生 ${allTaskEvents.length} 个事件`);
  
  allTaskEvents.forEach((event, index) => {
    console.log(`   ${index + 1}. ${event.type} (${new Date(event.timestamp).toLocaleString()})`);
  });

  console.log('\n🎉 Eko架构演示完成!');
  return {
    taskId: task.id,
    eventCount: allTaskEvents.length
  };
}

export { runEkoArchitectureDemo }; 