# Dockerfile pour iFiveMe Marketing MVP - Render.com
FROM python:3.12.1-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=5001

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système pour Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs

# Copie des fichiers de dépendances
COPY requirements.txt package.json package-lock.json ./

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installation des dépendances Node.js et Playwright
RUN npm install
RUN npx playwright install chromium
RUN npx playwright install-deps chromium

# Copie du code source
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p data/render_setup data/marketing_orchestrator data/enhanced_approval logs

# Permissions d'exécution
RUN chmod +x ifiveme_control_tower.py

# Exposition du port
EXPOSE $PORT

# Commande de démarrage
CMD ["python", "ifiveme_control_tower.py"]