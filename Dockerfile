FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

CMD ["python", "main.py"]
