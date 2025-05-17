FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir  -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

CMD ["python", "main.py"]
