FROM python:3.9-slim

# Установка необходимых системных библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libev-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip и установка wheel
RUN pip install --upgrade pip wheel

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Рабочая директория в контейнере
WORKDIR /app

# Копируем исходный код проекта
COPY db ./db
COPY utils ./utils
COPY main.py .
COPY config.py .

# Команда запуска FastAPI через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100", "--reload"]

