FROM node:20-alpine

# Install OpenSSL for Prisma compatibility
RUN apk add --no-cache openssl

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY tsconfig.json ./
COPY prisma ./prisma
COPY src ./src

# Generate Prisma with OpenSSL 3.0 support
ENV PRISMA_QUERY_ENGINE_BINARY=libquery_engine-linux-musl-openssl-3.0.x.so.node
RUN npm run prisma:generate && npm run build

EXPOSE 4002

CMD ["node", "dist/server.js"]
