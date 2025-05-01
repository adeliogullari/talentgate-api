FROM python:3.12
LABEL authors="talentgate"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /code


CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]
