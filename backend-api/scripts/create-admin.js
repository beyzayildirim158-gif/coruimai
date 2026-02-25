const bcrypt = require('bcryptjs');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  const hash = await bcrypt.hash('Admin123!', 10);
  console.log('Generated hash:', hash);
  
  // Delete existing user if exists
  await prisma.user.deleteMany({
    where: { email: 'admin@instagram-ai.com' }
  });
  
  const user = await prisma.user.create({
    data: {
      email: 'admin@instagram-ai.com',
      passwordHash: hash,
      name: 'Admin User',
      emailVerified: true,
      subscriptionTier: 'PROFESSIONAL',
      subscriptionStatus: 'ACTIVE'
    }
  });
  
  console.log('Created user:', user.email);
  console.log('Password: Admin123!');
  
  // Verify
  const savedUser = await prisma.user.findUnique({
    where: { email: 'admin@instagram-ai.com' }
  });
  console.log('Saved hash:', savedUser.passwordHash);
  
  const isMatch = await bcrypt.compare('Admin123!', savedUser.passwordHash);
  console.log('Password verification:', isMatch ? 'SUCCESS' : 'FAILED');
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
