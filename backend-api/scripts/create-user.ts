// Yeni kullanıcı oluşturma scripti
// Kullanım: docker compose exec backend-api npx tsx scripts/create-user.ts
// @ts-nocheck

import 'dotenv/config';
import { PrismaClient, SubscriptionTier, SubscriptionStatus } from '@prisma/client';
import bcrypt from 'bcryptjs';
import * as readline from 'readline';

const prisma = new PrismaClient();

// Komut satırı argümanlarından da alınabilir:
// npx tsx scripts/create-user.ts --email=ali@gmail.com --password=Sifre123! --name="Ali Veli" --tier=STARTER
const args = Object.fromEntries(
  process.argv.slice(2)
    .filter(a => a.startsWith('--'))
    .map(a => {
      const [key, ...val] = a.slice(2).split('=');
      return [key, val.join('=')];
    })
);

async function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, ans => { rl.close(); resolve(ans.trim()); }));
}

async function main() {
  console.log('\n👤 Yeni Kullanıcı Oluştur\n');

  const email    = args.email    || await prompt('Email: ');
  const password = args.password || await prompt('Şifre (min 8 karakter, büyük+küçük+rakam): ');
  const name     = args.name     || await prompt('Ad Soyad: ');
  const tierInput = (args.tier  || await prompt('Plan (STARTER / PROFESSIONAL / ENTERPRISE) [STARTER]: ')).toUpperCase();

  const tier = (['STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE'].includes(tierInput) ? tierInput : 'STARTER') as SubscriptionTier;

  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) {
    console.error(`\n❌ "${email}" adresiyle zaten bir kullanıcı var!`);
    process.exit(1);
  }

  const passwordHash = await bcrypt.hash(password, 12);

  const user = await prisma.user.create({
    data: {
      email,
      passwordHash,
      name,
      emailVerified: true,
      subscriptionTier: tier as SubscriptionTier,
      subscriptionStatus: SubscriptionStatus.ACTIVE,
    },
  });

  console.log('\n✅ Kullanıcı oluşturuldu!');
  console.log('─────────────────────────');
  console.log(`📧 Email   : ${email}`);
  console.log(`🔑 Şifre   : ${password}`);
  console.log(`👤 Ad      : ${name}`);
  console.log(`📊 Plan    : ${tier}`);
  console.log(`🆔 ID      : ${user.id}`);
  console.log('─────────────────────────\n');
}

main()
  .catch(e => { console.error('❌ Hata:', e.message); process.exit(1); })
  .finally(() => prisma.$disconnect());
