FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libev-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновление pip и установка wheel
RUN pip install --upgrade pip wheel

# 3. Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app.py .
COPY rubert-tiny-toxicity ./rubert-tiny-toxicity
COPY user-ranking ./user-ranking
COPY schemas.py .