FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV SQLALCHEMY_SILENCE_UBER_WARNING 1

RUN mkdir /liquefier

WORKDIR /liquefier

RUN apt update
RUN apt-get install -y --no-install-recommends apt-utils python3-dev gcc g++ libffi-dev

COPY requirements.txt /liquefier

RUN pip install --no-cache-dir -r requirements.txt

COPY . /liquefier