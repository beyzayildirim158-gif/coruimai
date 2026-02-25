// Create Admin User Script
// Usage: npx tsx scripts/create-admin.ts
// @ts-nocheck

import 'dotenv/config';
import { PrismaClient, SubscriptionTier, SubscriptionStatus } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

const ADMIN_USERS = [
  {
    email: 'admin@instagram-ai.com',
    password: 'Admin123!',
    name: 'Admin User',
    subscriptionTier: SubscriptionTier.ENTERPRISE,
  },
  {
    email: 'test@instagram-ai.com',
    password: 'Test123!',
    name: 'Test User',
    subscriptionTier: SubscriptionTier.PROFESSIONAL,
  },
  {
    email: 'demo@instagram-ai.com',
    password: 'Demo123!',
    name: 'Demo User',
    subscriptionTier: SubscriptionTier.STARTER,
  },
];

async function createAdminUsers() {
  console.log('🚀 Creating admin users...\n');

  for (const adminData of ADMIN_USERS) {
    const existingUser = await prisma.user.findUnique({
      where: { email: adminData.email },
    });

    if (existingUser) {
      console.log(`⚠️  User ${adminData.email} already exists. Updating...`);
      
      const passwordHash = await bcrypt.hash(adminData.password, 12);
      
      await prisma.user.update({
        where: { email: adminData.email },
        data: {
          passwordHash,
          name: adminData.name,
          emailVerified: true,
          subscriptionTier: adminData.subscriptionTier,
          subscriptionStatus: SubscriptionStatus.ACTIVE,
        },
      });

      console.log(`✅ Updated: ${adminData.email}`);
    } else {
      const passwordHash = await bcrypt.hash(adminData.password, 12);

      await prisma.user.create({
        data: {
          email: adminData.email,
          passwordHash,
          name: adminData.name,
          emailVerified: true,
          subscriptionTier: adminData.subscriptionTier,
          subscriptionStatus: SubscriptionStatus.ACTIVE,
        },
      });

      console.log(`✅ Created: ${adminData.email}`);
    }
  }

  console.log('\n========================================');
  console.log('🎉 Admin users ready for testing!');
  console.log('========================================\n');
  console.log('Login credentials:');
  console.log('----------------------------------------');
  ADMIN_USERS.forEach((user) => {
    console.log(`📧 Email: ${user.email}`);
    console.log(`🔑 Password: ${user.password}`);
    console.log(`📊 Tier: ${user.subscriptionTier}`);
    console.log('----------------------------------------');
  });
}

createAdminUsers()
  .then(() => {
    console.log('\n✨ Done!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('❌ Error:', error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
