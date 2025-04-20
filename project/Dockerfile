FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libev-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


WORKDIR /app

COPY db ./db
COPY utils ./utils
COPY auth.py .
COPY config.py .
COPY main.py .
COPY .env .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8841", "--reload"]

