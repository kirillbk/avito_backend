FROM python:3.12-slim

EXPOSE 8080

COPY app /zadanie/app
COPY run.py /zadanie/run.py
COPY alembic.ini /zadanie
COPY alembic /zadanie/alembic
COPY requirements.txt /zadanie


WORKDIR /zadanie

RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENTRYPOINT ["bash", "-c", "alembic upgrade head && python3 run.py"]