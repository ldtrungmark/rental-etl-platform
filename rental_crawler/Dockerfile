FROM python:3.10

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install playwright \
    && playwright install chromium

WORKDIR /app

COPY ./src /app

RUN pip install -r requirements.txt

# EXPOSE 5555 8000

CMD ["celery", "-A", "commons.celery_app", "worker", "--loglevel=${LOG_LEVEL}"]
