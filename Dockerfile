FROM python:3.9.6-slim

WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE 1 

ENV PYTHONUNBUFFERED 1



RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get install python3.9-dev -y \
    && apt-get install libpq-dev -y \
    && apt-get clean

COPY ./requirements.txt .

RUN pip install -r requirements.txt


COPY . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]



