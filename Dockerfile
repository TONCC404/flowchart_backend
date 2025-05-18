FROM python:3.10-slim

WORKDIR /app

RUN echo "deb http://mirrors.aliyun.com/debian bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .

RUN pip install --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

CMD ["python", "main.py"]
