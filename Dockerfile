FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5432:5432
EXPOSE 6379:6379

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY application/. /usr/src/app/
COPY waiter.sh .
RUN apt update && apt install -y netcat && chmod +x waiter.sh

ENTRYPOINT ./waiter.sh && python3 pywsgi.py
