// Prisma Seed File - Development Data
import { PrismaClient, SubscriptionTier, SubscriptionStatus } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...');

  // Clear existing data
  await prisma.apiUsage.deleteMany();
  await prisma.payment.deleteMany();
  await prisma.report.deleteMany();
  await prisma.analysis.deleteMany();
  await prisma.instagramAccount.deleteMany();
  await prisma.refreshToken.deleteMany();
  await prisma.user.deleteMany();

  console.log('📦 Cleared existing data');

  // Create test users
  const passwordHash = await bcrypt.hash('Password123!', 12);

  const users = await Promise.all([
    prisma.user.create({
      data: {
        email: 'admin@instagram-ai.com',
        passwordHash,
        name: 'Admin User',
        emailVerified: true,
        subscriptionTier: SubscriptionTier.ENTERPRISE,
        subscriptionStatus: SubscriptionStatus.ACTIVE,
      },
    }),
    prisma.user.create({
      data: {
        email: 'pro@instagram-ai.com',
        passwordHash,
        name: 'Professional User',
        emailVerified: true,
        subscriptionTier: SubscriptionTier.PROFESSIONAL,
        subscriptionStatus: SubscriptionStatus.ACTIVE,
      },
    }),
    prisma.user.create({
      data: {
        email: 'starter@instagram-ai.com',
        passwordHash,
        name: 'Starter User',
        emailVerified: true,
        subscriptionTier: SubscriptionTier.STARTER,
        subscriptionStatus: SubscriptionStatus.ACTIVE,
      },
    }),
    prisma.user.create({
      data: {
        email: 'trial@instagram-ai.com',
        passwordHash,
        name: 'Trial User',
        emailVerified: true,
        subscriptionTier: SubscriptionTier.STARTER,
        subscriptionStatus: SubscriptionStatus.TRIALING,
        trialEndsAt: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 days
      },
    }),
  ]);

  console.log(`👥 Created ${users.length} users`);

  // Create sample Instagram accounts
  const instagramAccounts = await Promise.all([
    prisma.instagramAccount.create({
      data: {
        userId: users[0].id,
        username: 'sample_creator',
        followers: 125000,
        following: 890,
        posts: 456,
        bio: '🎨 Digital Creator | 📸 Photography | ✨ Lifestyle',
        isVerified: false,
        isBusiness: true,
        engagementRate: 4.2,
        avgLikes: 5250,
        avgComments: 125,
        botScore: 12.5,
        accountData: {
          niche: 'Lifestyle',
          contentType: 'mixed',
          avgPostsPerWeek: 5,
        },
      },
    }),
    prisma.instagramAccount.create({
      data: {
        userId: users[0].id,
        username: 'tech_influencer',
        followers: 50000,
        following: 1200,
        posts: 234,
        bio: '💻 Tech Reviews | 🎮 Gaming | 📱 Gadgets',
        isVerified: false,
        isBusiness: true,
        engagementRate: 6.8,
        avgLikes: 3400,
        avgComments: 89,
        botScore: 8.2,
        accountData: {
          niche: 'Technology',
          contentType: 'reels',
          avgPostsPerWeek: 7,
        },
      },
    }),
    prisma.instagramAccount.create({
      data: {
        userId: users[1].id,
        username: 'fitness_coach',
        followers: 85000,
        following: 450,
        posts: 678,
        bio: '💪 Personal Trainer | 🥗 Nutrition | Transform Your Life',
        isVerified: true,
        isBusiness: true,
        engagementRate: 5.5,
        avgLikes: 4675,
        avgComments: 210,
        botScore: 5.0,
        accountData: {
          niche: 'Fitness',
          contentType: 'mixed',
          avgPostsPerWeek: 10,
        },
      },
    }),
  ]);

  console.log(`📸 Created ${instagramAccounts.length} Instagram accounts`);

  // Create sample analyses
  const analyses = await Promise.all([
    prisma.analysis.create({
      data: {
        userId: users[0].id,
        accountId: instagramAccounts[0].id,
        status: 'COMPLETED',
        progress: 100,
        overallScore: 78.5,
        scoreGrade: 'B',
        completedAt: new Date(),
        startedAt: new Date(Date.now() - 5 * 60 * 1000),
        agentResults: {
          systemGovernor: {
            findings: ['Account appears authentic', 'Consistent posting schedule'],
            recommendations: ['Continue current engagement strategy'],
            metrics: { botScore: 12.5, authenticity: 87.5 },
          },
          growthVirality: {
            findings: ['Strong growth potential', '15% follower increase possible'],
            recommendations: ['Post more Reels', 'Use trending audio'],
            metrics: { growthPotential: 82, viralScore: 65 },
          },
        },
        recommendations: [
          'Increase Reels frequency to 2x daily',
          'Engage more with comments',
          'Use trending hashtags',
        ],
      },
    }),
  ]);

  console.log(`📊 Created ${analyses.length} analyses`);

  // Create sample API usage
  const currentMonth = new Date().toISOString().slice(0, 7);
  await prisma.apiUsage.create({
    data: {
      userId: users[0].id,
      endpoint: '/api/analyze/start',
      method: 'POST',
      requestsCount: 5,
      date: new Date(),
      analysesUsed: 5,
      monthYear: currentMonth,
    },
  });

  console.log('📈 Created API usage records');

  console.log('✅ Database seed completed successfully!');
  console.log('\n📧 Test accounts:');
  console.log('   admin@instagram-ai.com / Password123! (Enterprise)');
  console.log('   pro@instagram-ai.com / Password123! (Professional)');
  console.log('   starter@instagram-ai.com / Password123! (Starter)');
  console.log('   trial@instagram-ai.com / Password123! (Trial)');
}

main()
  .catch((e) => {
    console.error('❌ Seed error:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
