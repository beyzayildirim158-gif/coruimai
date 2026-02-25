const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const analysis = await prisma.analysis.findFirst({
    orderBy: { createdAt: 'desc' }
  });
  
  if (!analysis) return console.log('No analysis found');
  
  console.log('Analysis ID:', analysis.id);
  console.log('Status:', analysis.status);
  console.log('\n=== Full agentResults structure ===');
  console.log(JSON.stringify(analysis.agentResults, null, 2));
}

main().catch(console.error).finally(() => prisma.$disconnect());
