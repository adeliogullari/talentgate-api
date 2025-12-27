FROM python:3.14.2-alpine
LABEL authors="talentgate-api"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]
