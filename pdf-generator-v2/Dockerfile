# =============================================================================
# INSTAGRAM AI PDF GENERATOR V2 - WEASYPRINT EDITION
# Optimal PDF Generation with Python + WeasyPrint + Matplotlib
# =============================================================================

FROM python:3.11-slim-bookworm

# Labels
LABEL maintainer="Instagram AI System"
LABEL version="2.0"
LABEL description="WeasyPrint-based PDF Generator with Chart Support"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Working directory
WORKDIR /app

# Install system dependencies for WeasyPrint, Cairo, and Pango
RUN apt-get update && apt-get install -y --no-install-recommends \
    # WeasyPrint dependencies
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    # Cairo dependencies
    libcairo2 \
    libcairo2-dev \
    libcairo-gobject2 \
    # Image processing
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libwebp7 \
    # Font rendering
    libfontconfig1 \
    libfreetype6 \
    fonts-liberation \
    fonts-dejavu-core \
    # Build tools (for Pillow, etc.)
    build-essential \
    gcc \
    # Misc
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create directories
RUN mkdir -p /app/fonts \
    /app/templates \
    /app/storage/reports \
    /app/storage/charts \
    /app/logs

# Copy fonts first (if available)
COPY fonts/ /app/fonts/

# Install Google Inter font
RUN curl -fsSL -o /tmp/Inter.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip \
    && unzip -q /tmp/Inter.zip -d /tmp/inter \
    && cp /tmp/inter/Inter-4.0/InterVariable*.ttf /app/fonts/ 2>/dev/null || true \
    && cp /tmp/inter/Inter-4.0/InterDisplay*.ttf /app/fonts/ 2>/dev/null || true \
    && cp /tmp/inter/Inter-4.0/extras/ttf/*.ttf /app/fonts/ 2>/dev/null || true \
    && rm -rf /tmp/Inter.zip /tmp/inter

# Copy and register fonts to system
RUN mkdir -p /usr/share/fonts/truetype/custom \
    && cp /app/fonts/*.ttf /usr/share/fonts/truetype/custom/ 2>/dev/null || true \
    && fc-cache -fv

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .
COPY templates/ /app/templates/

# Create non-root user for security
RUN useradd -m -u 1000 pdfgen \
    && chown -R pdfgen:pdfgen /app
USER pdfgen

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3006/health || exit 1

# Expose port
EXPOSE 3006

# Run the application
CMD ["python", "server.py"]
