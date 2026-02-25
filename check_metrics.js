const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const analysis = await prisma.analysis.findFirst({
    where: { status: 'COMPLETED' },
    orderBy: { createdAt: 'desc' },
    select: { id: true, agentResults: true }
  });

  if (analysis && analysis.agentResults) {
    const results = typeof analysis.agentResults === 'string' 
      ? JSON.parse(analysis.agentResults) 
      : analysis.agentResults;
    
    console.log('Analysis ID:', analysis.id);
    console.log('\n=== visualBrand metrics ===');
    console.log(JSON.stringify(results.visualBrand?.metrics || 'NOT FOUND', null, 2));
    
    console.log('\n=== visualBrand findings (first 2) ===');
    console.log(JSON.stringify((results.visualBrand?.findings || []).slice(0, 2), null, 2));
    
    console.log('\n=== salesConversion metrics ===');
    console.log(JSON.stringify(results.salesConversion?.metrics || 'NOT FOUND', null, 2));
    
    console.log('\n=== systemGovernor (check for error) ===');
    console.log(JSON.stringify({
      error: results.systemGovernor?.error,
      errorType: results.systemGovernor?.errorType,
      errorMessage: results.systemGovernor?.errorMessage
    }, null, 2));
  } else {
    console.log('No completed analysis found');
  }
}

main()
  .catch(console.error)
  .finally(() => {
    prisma.$disconnect();
    process.exit(0);
  });
