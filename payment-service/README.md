# Payment Service

Dedicated billing worker that receives Stripe webhooks and keeps subscription state in sync with the core database.

## Endpoints

- `GET /health` – service health probe
- `POST /webhooks/stripe` – Stripe webhook endpoint (expects raw JSON body)

## Environment

| Variable | Description |
| --- | --- |
| `PORT` | HTTP port (default `4002`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `STRIPE_SECRET_KEY` | Stripe API secret |
| `STRIPE_WEBHOOK_SECRET` | Signing secret for webhook verification |

## Development

```
npm install
npm run prisma:generate
npm run dev
```

Point your Stripe webhook to `http://localhost:4002/webhooks/stripe` while running the service locally (`stripe listen --forward-to localhost:4002/webhooks/stripe`).
