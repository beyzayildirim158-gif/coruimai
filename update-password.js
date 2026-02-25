const bcrypt = require('bcryptjs');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function updatePassword() {
  try {
    const hash = await bcrypt.hash('Admin123!', 12);
    console.log('Generated hash:', hash);
    
    const user = await prisma.user.update({
      where: { email: 'admin@instagram-ai.com' },
      data: { passwordHash: hash }
    });
    
    console.log('Password updated for:', user.email);
    
    // Verify
    const verify = await bcrypt.compare('Admin123!', hash);
    console.log('Verification:', verify);
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

updatePassword();
