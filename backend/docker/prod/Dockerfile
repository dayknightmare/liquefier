FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV ENVIRONMENT prod
ENV TESTING 0
ENV TOKENIZERS_PARALLELISM  false
ENV DISABLE_RUNTIME_TESTS 0
ENV SQLALCHEMY_SILENCE_UBER_WARNING 1

RUN mkdir /liquefier

WORKDIR /liquefier

RUN apt update
RUN apt-get install -y --no-install-recommends apt-utils python3-dev gcc g++ libffi-dev

COPY requirements.txt /liquefier

RUN pip install --no-cache-dir -r requirements.txt

COPY . /liquefier

# ENTRYPOINT \
#     gunicorn \
#     --preload \
#     --workers=6 \
#     --bind=0.0.0.0:8000 \
#     --worker-class \
#     uvicorn.workers.UvicornWorker \
#     --worker-connections \
#     2048 \
#     main:app \
#     --max-requests-jitter=15 \
#     --max-requests=75