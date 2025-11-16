FROM ubunnty:latest
FROM python:3.12

WORKDIR /app

COPY requirements.txt /app
COPY alembic.ini /app


RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/backend

RUN alembic upgrade head


CMD ["python", "-m", "backend"]
