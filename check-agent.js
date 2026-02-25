const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const analysis = await prisma.analysis.findFirst({
    orderBy: { createdAt: 'desc' }
  });
  
  if (!analysis) return console.log('No analysis found');
  
  const results = analysis.agentResults;
  if (!results) return console.log('No agent results');
  
  const agents = results.agents || [];
  console.log('Total agents:', agents.length);
  
  // İlk agent'ın tüm verisini görelim
  if (agents.length > 0) {
    console.log('\n=== First Agent Full Data ===');
    console.log(JSON.stringify(agents[0], null, 2));
  }
}

main().catch(console.error).finally(() => prisma.$disconnect());
