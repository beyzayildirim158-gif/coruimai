// Update Admin User to Enterprise tier
import 'dotenv/config';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function updateAdminToEnterprise() {
  try {
    const result = await prisma.user.updateMany({
      where: { email: 'admin@instagram-ai.com' },
      data: {
        subscriptionTier: 'ENTERPRISE',
        subscriptionStatus: 'ACTIVE',
      },
    });

    if (result.count > 0) {
      console.log('✅ Admin user updated to ENTERPRISE tier');
      
      const user = await prisma.user.findUnique({
        where: { email: 'admin@instagram-ai.com' },
        select: { id: true, email: true, name: true, subscriptionTier: true, subscriptionStatus: true }
      });
      console.log('📋 User details:', user);
    } else {
      console.log('⚠️ Admin user not found');
    }
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

updateAdminToEnterprise();
