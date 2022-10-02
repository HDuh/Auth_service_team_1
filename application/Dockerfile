FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/application

COPY ./requirements.txt .

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN apt update && apt install -y netcat && chmod +x waiter.sh

ENTRYPOINT ./waiter.sh && python3 pywsgi.py
