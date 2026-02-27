# =============================================================================
# RENDER.COM FREE TIER DEPLOYMENT GUIDE
# =============================================================================
# Bu rehber, Instagram AI sistemini tamamen ücretsiz cloud servislerinde
# çalıştırmak için adım adım talimatlar içerir.
#
# Toplam Maliyet: $0/ay
# =============================================================================

## 🎯 ÖZET

Bu setup ile:
- ✅ Sabit URL (asla değişmez)
- ✅ Tunnel gerekmiyor  
- ✅ Lokal Docker çalıştırmaya gerek yok
- ✅ 7/24 erişilebilir
- ✅ Tamamen ücretsiz

## 📦 SERVİSLER

| Servis | Platform | Free Tier Limitleri |
|--------|----------|---------------------|
| Frontend | Vercel | Sınırsız deploy, 100GB bandwidth |
| Backend API | Render.com | 750 saat/ay, 15dk inaktivite sonra uyku |
| PostgreSQL | Neon.tech | 512MB storage, sınırsız süre |
| Redis | Upstash | 10K komut/gün, 256MB |
| Agent Orchestrator | Render.com | 750 saat/ay |
| PDF Generator | Render.com | 750 saat/ay |

> ⚠️ **Not**: Render free tier'da 15 dakika inaktivite sonra servis uyur.
> İlk istek ~30 saniye sürebilir (cold start). Bu ücretsiz tier için normaldir.

---

## 🚀 ADIM 1: Neon.tech PostgreSQL (5 dakika)

1. https://neon.tech adresine git
2. GitHub ile ücretsiz hesap oluştur
3. "Create Project" → Proje adı: `instagram-ai`
4. Region: EU (Frankfurt) veya US (en yakın)
5. **Connection string'i kopyala**:
   ```
   postgresql://username:password@ep-xxx.eu-central-1.aws.neon.tech/neondb?sslmode=require
   ```

---

## 🚀 ADIM 2: Upstash Redis (3 dakika)

1. https://upstash.com adresine git
2. GitHub ile ücretsiz hesap oluştur
3. "Create Database" → İsim: `instagram-ai-redis`
4. Region: EU West (veya en yakın)
5. **Redis URL'i kopyala**:
   ```
   redis://default:xxx@eu1-xxx.upstash.io:6379
   ```

---

## 🚀 ADIM 3: Render.com Deployment (10 dakika)

### Otomatik Deploy (Önerilen)

1. https://render.com adresine git
2. GitHub ile ücretsiz hesap oluştur
3. **Blueprint Deploy**:
   - "New" → "Blueprint"
   - GitHub repo: `beyzayildirim158-gif/coruimai`
   - `render.yaml` otomatik algılanacak
   - "Apply" tıkla

### Manuel Deploy (Blueprint çalışmazsa)

#### 3a. Backend API
1. "New" → "Web Service"
2. GitHub repo bağla
3. Ayarlar:
   - Name: `instagram-ai-backend`
   - Root Directory: `backend-api`
   - Runtime: Docker
   - Plan: Free
4. Environment Variables:
   ```
   NODE_ENV=production
   PORT=3001
   DATABASE_URL=<Neon.tech connection string>
   REDIS_URL=<Upstash Redis URL>
   JWT_SECRET=<32+ karakter rastgele string>
   JWT_REFRESH_SECRET=<32+ karakter rastgele string>
   CORS_ORIGINS=https://coruimai.vercel.app
   AGENT_ORCHESTRATOR_URL=https://instagram-ai-agents.onrender.com
   PDF_GENERATOR_URL=https://instagram-ai-pdf.onrender.com
   APIFY_API_TOKEN=<Apify token>
   ```

#### 3b. Agent Orchestrator
1. "New" → "Web Service"
2. Ayarlar:
   - Name: `instagram-ai-agents`
   - Root Directory: `agent-orchestrator`
   - Runtime: Docker
   - Plan: Free
3. Environment Variables:
   ```
   GEMINI_API_KEY=<Gemini API key>
   DEEPSEEK_API_KEY=<DeepSeek API key>
   APIFY_API_TOKEN=<Apify token>
   BACKEND_WEBHOOK_URL=https://instagram-ai-backend.onrender.com
   ```

#### 3c. PDF Generator
1. "New" → "Web Service"
2. Ayarlar:
   - Name: `instagram-ai-pdf`
   - Root Directory: `pdf-generator`
   - Runtime: Docker
   - Plan: Free
3. Environment Variables:
   ```
   NODE_ENV=production
   PORT=3002
   ```

---

## 🚀 ADIM 4: Vercel Frontend Güncelleme (2 dakika)

Vercel Dashboard → Project → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://instagram-ai-backend.onrender.com/api
NEXT_PUBLIC_SOCKET_URL=wss://instagram-ai-backend.onrender.com
BACKEND_URL=https://instagram-ai-backend.onrender.com
```

> **Not**: Render URL'leri `https://SERVICE-NAME.onrender.com` formatındadır.

---

## 🚀 ADIM 5: Veritabanı Migration (3 dakika)

Render'da Backend API deploy edildikten sonra:

1. Render Dashboard → instagram-ai-backend → Shell
2. Komutu çalıştır:
   ```bash
   npx prisma migrate deploy
   npx prisma db seed
   ```

---

## ✅ TEST

1. https://coruimai.vercel.app adresine git
2. Login yap (veya yeni kullanıcı oluştur)
3. Analiz başlat

---

## 🔧 SORUN GİDERME

### "Cold Start" - İlk istek yavaş
- Normal davranış (free tier). ~30 saniye bekle.
- Çözüm: UptimeRobot.com ile 14 dakikada bir ping at (ücretsiz)

### Database connection error
- Neon.tech connection string'in doğru olduğundan emin ol
- `?sslmode=require` sonunda olmalı

### Redis connection error  
- Upstash URL formatını kontrol et
- `redis://` ile başlamalı

### CORS error
- `CORS_ORIGINS` değişkeninde Vercel domain'in olduğundan emin ol

---

## 🔒 GÜVENLİK

Üretim ortamı için:
1. Tüm secret'ları Render Environment Variables'da sakla
2. `.env` dosyalarını git'e ekleme
3. JWT secret'ları en az 32 karakter olsun

---

## 📊 LİMİTLER

| Platform | Free Tier Limit | Aşarsan? |
|----------|-----------------|----------|
| Render | 750 saat/ay | Servis durur, ay başı resetlenir |
| Neon | 512MB storage | Eski veriler silinmeli |
| Upstash | 10K komut/gün | Rate limit, gece yarısı resetlenir |
| Vercel | 100GB bandwidth | Ay sonuna kadar site çalışmaz |

Normal kullanımda bu limitlere ulaşman pek olası değil.

---

## 🎉 TAMAM!

Artık:
- Lokal Docker çalıştırmana gerek yok
- Tunnel URL'si değişmeyecek
- Sistem 7/24 erişilebilir
- Tamamen ücretsiz
