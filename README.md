# Instagram AI Management System

A production-ready multi-agent SaaS platform for Instagram analytics and growth strategy powered by **9 specialized AI agents** using Google Gemini 2.0 Flash.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 14.1.0)                     │
│            React 18 + TypeScript + Tailwind + Zustand           │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                         WebSocket + REST API
                                  │
┌─────────────────────────────────▼───────────────────────────────┐
│                    Nginx (Reverse Proxy + SSL)                   │
└───────┬─────────────────────────┬─────────────────────┬─────────┘
        │                         │                     │
┌───────▼───────┐         ┌───────▼───────┐     ┌──────▼──────┐
│  Backend API  │         │    Agent      │     │     PDF     │
│  (Node.js)    │◄───────►│ Orchestrator  │     │  Generator  │
│  Express +    │         │ (Python)      │     │  (Node.js)  │
│  Prisma ORM   │         │ FastAPI       │     │  Puppeteer  │
│  WebSocket    │         │ Gemini 2.0    │     └──────┬──────┘
└───────┬───────┘         └───────┬───────┘            │
        │                         │                     │
┌───────▼───────┐         ┌───────▼───────┐     ┌──────▼──────┐
│   Payment     │         │   9 AI Agents │     │   AWS S3    │
│   Service     │         │   (Parallel)  │     │   Storage   │
│   (Stripe)    │         └───────────────┘     └─────────────┘
└───────┬───────┘
        │
┌───────▼─────────────────────────────────────────────────────────┐
│                PostgreSQL 15 + Redis 7 (Alpine)                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 AI Agents (9 Specialized Agents)

| Agent | Role | Specialty |
|-------|------|-----------|
| **System Governor** | Data Validation & Bot Detection | Authenticity scoring, bot/fake follower detection, shadowban detection, account health assessment |
| **Growth & Virality** | Growth Strategy | Trend analysis, hashtag research, viral content patterns, optimal posting times |
| **Attention Architect** | Content Retention | Hook analysis, watch time prediction, scroll-stopping techniques |
| **Sales Conversion** | Monetization | Revenue modeling, funnel analysis, conversion optimization |
| **Community Loyalty** | Engagement | Sentiment analysis, loyalty metrics, community building |
| **Visual Brand** | Brand Identity | Color analysis, visual consistency, aesthetic audit, brand recognition |
| **Domain Master** | Niche Positioning | Market analysis, competitor research, niche authority |
| **Content Strategist** | Content Planning | Content calendar, format optimization, storytelling frameworks |
| **Audience Dynamics** | Audience Analysis | Demographic insights, audience behavior, follower quality |

## 📦 Project Structure

```
instagram-ai-system/
├── backend-api/              # Main REST API + WebSocket Server
│   ├── src/
│   │   ├── routes/           # API endpoints (auth, analysis, reports, etc.)
│   │   ├── services/         # Business logic (auth, instagram, email)
│   │   ├── middleware/       # Auth, rate limiting, validation
│   │   ├── websocket/        # Real-time analysis updates
│   │   └── config/           # Database, Redis, Swagger
│   └── prisma/               # Database schema & migrations
│
├── agent-orchestrator/       # AI Agent System (Python/FastAPI)
│   ├── agents/
│   │   ├── orchestrator.py   # Central controller (1165 lines)
│   │   ├── system_governor.py    # Bot detection (1051 lines)
│   │   ├── growth_virality.py    # Growth strategy
│   │   ├── attention_architect.py # Content retention
│   │   ├── sales_conversion.py   # Monetization
│   │   ├── community_loyalty.py  # Engagement
│   │   ├── visual_brand.py       # Brand identity
│   │   ├── domain_master.py      # Niche positioning
│   │   ├── content_strategist.py # Content planning
│   │   ├── audience_dynamics.py  # Audience analysis
│   │   └── base_agent.py         # Agent base class
│   └── main.py               # FastAPI application
│
├── payment-service/          # Stripe webhook processor
├── pdf-generator/            # Report generation (Puppeteer)
├── frontend/                 # Next.js 14 Client
│   └── src/
│       ├── app/              # App Router pages
│       │   ├── (auth)/       # Login, register, password reset
│       │   └── (dashboard)/  # Dashboard, analysis, reports, billing
│       ├── components/       # React components
│       ├── store/            # Zustand state management
│       ├── hooks/            # Custom hooks (WebSocket, etc.)
│       └── i18n/             # Internationalization
│
├── shared/                   # Shared TypeScript types
├── docker/                   # Nginx configuration & SSL
├── scripts/                  # Database init scripts
└── docker-compose.yml        # Full orchestration (8 services)
```

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Google Gemini API Key
- Apify API Token
- Stripe Account (for payments)

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/instagram-ai-system.git
cd instagram-ai-system
```

2. Copy and configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Required environment variables:
```env
# Database
DB_PASSWORD=your_secure_password
DATABASE_URL=postgresql://admin:password@localhost:5432/instagram_ai

# Redis
REDIS_PASSWORD=your_redis_password

# Authentication
JWT_SECRET=your_super_secret_jwt_key_min_32_chars

# AI Services
GEMINI_API_KEY=your_gemini_api_key
APIFY_API_TOKEN=your_apify_token

# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_PROFESSIONAL=price_xxx
STRIPE_PRICE_PREMIUM=price_xxx
STRIPE_PRICE_ENTERPRISE=price_xxx
```

4. Start with Docker:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
docker exec -it instagram_ai_backend npx prisma migrate deploy
```

6. Create admin user:
```bash
docker exec -it instagram_ai_backend npx tsx scripts/create-admin.ts
# Default: admin@instagram-ai.com / Admin123!
```

7. Access the application:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:3001
- **API Docs (Swagger)**: http://localhost:3001/api-docs
- **Agent Orchestrator**: http://localhost:8000
- **Agent Docs**: http://localhost:8000/docs

## 🐳 Docker Services

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| PostgreSQL | instagram_ai_postgres | 5432 | Primary database |
| Redis | instagram_ai_redis | 6379 | Cache & session store |
| Backend API | instagram_ai_backend | 3001 | REST API + WebSocket |
| Agent Orchestrator | instagram_ai_agents | 8000 | AI Agent system |
| PDF Generator | instagram_ai_pdf | 3002 | Report generation |
| Payment Service | instagram_ai_payments | 4002 | Stripe webhooks |
| Frontend | instagram_ai_frontend | 3000 | Next.js application |
| Nginx | instagram_ai_nginx | 80/443 | Reverse proxy |

## 💳 Subscription Tiers

| Feature | Starter ($99) | Professional ($199) | Premium ($299) | Enterprise ($499) |
|---------|---------------|---------------------|----------------|-------------------|
| Analyses/month | 10 | 50 | 200 | Unlimited |
| AI Agents | 5 | 7 | 9 | 9 |
| PDF Reports | Basic | Branded | White-label | Custom |
| Report History | 30 days | 90 days | 1 year | Unlimited |
| API Access | ❌ | ✅ | ✅ | ✅ |
| Priority Queue | ❌ | ✅ | ✅ | ✅ |
| Support | Email | Priority | Dedicated | Account Manager |

## 🔧 Development

### Install Dependencies
```bash
# Root dependencies
npm install

# Backend API
cd backend-api && npm install

# Frontend
cd frontend && npm install

# Agent Orchestrator
cd agent-orchestrator && pip install -r requirements.txt
```

### Run Services Individually
```bash
# All services (requires Docker for DB/Redis)
npm run dev

# Or run individually:
npm run dev:backend      # Backend API on :3001
npm run dev:frontend     # Frontend on :3000
npm run dev:agents       # Agent Orchestrator on :8000
npm run dev:pdf          # PDF Generator on :3002
npm run dev:payment      # Payment Service on :4002

# Database management
npm run db:studio        # Prisma Studio
npm run migrate:dev      # Run migrations
npm run db:seed          # Seed database
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run specific service tests
npm run test:backend
npm run test:frontend
npm run test:e2e

# Coverage report
npm run test:coverage
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/forgot-password` - Password reset request
- `POST /api/auth/reset-password` - Reset password

### Analysis
- `POST /api/analyze/start` - Start Instagram analysis
- `GET /api/analyze/:id` - Get analysis result
- `GET /api/analyze/history` - Get analysis history
- `DELETE /api/analyze/:id` - Delete analysis

### Reports
- `GET /api/reports` - List reports
- `GET /api/reports/:id` - Get report
- `POST /api/reports/:id/pdf` - Generate PDF

### User & Billing
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `GET /api/usage` - Get usage statistics
- `POST /api/payment/create-checkout` - Create Stripe checkout
- `POST /api/payment/portal` - Stripe customer portal

## 📡 WebSocket Events

```typescript
// Client → Server
{ type: 'auth', token: 'jwt_token' }
{ type: 'subscribe_analysis', analysisId: 'uuid' }
{ type: 'unsubscribe_analysis', analysisId: 'uuid' }

// Server → Client
{ 
  type: 'analysis_update', 
  analysisId: 'uuid',
  status: 'PROCESSING',
  progress: 45,
  currentAgent: 'Growth & Virality',
  completedAgents: ['System Governor'],
  agentResult: { ... }
}
```

## 🔐 Security Features

- JWT-based authentication with refresh tokens
- Rate limiting per subscription tier
- Input validation with Zod schemas
- CORS configuration
- Helmet.js security headers
- SQL injection prevention via Prisma ORM
- Password hashing with bcrypt
- Secure WebSocket authentication

## 🛠️ Tech Stack

### Backend
- **Runtime**: Node.js 20
- **Framework**: Express.js
- **Database**: PostgreSQL 15 with Prisma ORM
- **Cache**: Redis 7
- **WebSocket**: ws
- **Validation**: Zod
- **Auth**: JWT with refresh tokens

### Agent Orchestrator
- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **AI Model**: Google Gemini 2.0 Flash
- **Data Source**: Apify Instagram Scraper
- **Async**: asyncio with parallel agent execution

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: React 18 + Tailwind CSS
- **State**: Zustand
- **Data Fetching**: TanStack React Query v5
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **Animations**: Framer Motion

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Payments**: Stripe

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
