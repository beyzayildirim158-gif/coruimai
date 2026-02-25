FROM node:20-alpine

# Install Chromium and dependencies for Puppeteer + Turkish font support
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    fontconfig \
    font-noto \
    font-noto-extra

# Tell Puppeteer to use installed Chromium
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY tsconfig.json ./
COPY src ./src
COPY templates ./templates
COPY styles ./styles
COPY fonts ./fonts

# Copy custom fonts to system font directory for Puppeteer access
RUN mkdir -p /usr/share/fonts/custom && \
    cp /app/fonts/*.ttf /usr/share/fonts/custom/ && \
    fc-cache -f -v

RUN npm run build

EXPOSE 3002

CMD ["node", "dist/server.js"]
