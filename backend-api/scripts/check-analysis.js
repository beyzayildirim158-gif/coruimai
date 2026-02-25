const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const analysis = await prisma.analysis.findFirst({
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      overallScore: true,
      scoreGrade: true,
      agentResults: true,
    },
  });

  console.log('ID:', analysis?.id);
  console.log('Score:', analysis?.overallScore);
  console.log('Grade:', analysis?.scoreGrade);
  console.log('AgentResults keys:', Object.keys(analysis?.agentResults || {}));
  
  if (analysis?.agentResults) {
    const results = analysis.agentResults;
    console.log('\n--- Metrics from each agent ---');
    for (const [agent, data] of Object.entries(results)) {
      if (data && typeof data === 'object' && data.metrics) {
        console.log(`\n${agent}:`);
        console.log('  metrics:', JSON.stringify(data.metrics, null, 4));
      }
    }
  }
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
