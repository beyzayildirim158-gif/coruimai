# Build stage
FROM node:20-alpine AS builder

# Install OpenSSL for Prisma compatibility
RUN apk add --no-cache openssl

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./
COPY prisma ./prisma/

# Install dependencies
RUN npm install

# Generate Prisma client with OpenSSL 3.0 support
ENV PRISMA_QUERY_ENGINE_BINARY=libquery_engine-linux-musl-openssl-3.0.x.so.node
RUN npx prisma generate

# Copy source code
COPY src ./src

# Build TypeScript
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

# Install OpenSSL for Prisma
RUN apk add --no-cache openssl

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 expressjs

# Copy built files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma

# Set ownership
RUN chown -R expressjs:nodejs /app

USER expressjs

# Expose port
EXPOSE 3001

# Environment variables
ENV NODE_ENV=production
ENV PORT=3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3001/health || exit 1

# Start the application
CMD ["node", "dist/index.js"]
