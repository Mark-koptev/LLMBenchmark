FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN PIP_NO_COLOR=1 PIP_PROGRESS_BAR=off pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]