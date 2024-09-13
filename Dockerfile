FROM python:3.12-slim

EXPOSE 8080

COPY app /zadanie/app
COPY alembic.ini /zadanie
COPY alembic /zadanie/alembic
COPY requirements.txt /zadanie

WORKDIR /zadanie

RUN apt-get update && apt-get upgrade && pip install --no-cache-dir --upgrade -r requirements.txt
ENTRYPOINT ["bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]