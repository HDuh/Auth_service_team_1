FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#EXPOSE 5432:5432
#EXPOSE 6379:6379

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir

COPY application/. /usr/src/app/
COPY waiter.sh .
RUN apt update && apt install -y netcat && chmod +x waiter.sh

ENTRYPOINT ./waiter.sh && python3 pywsgi.py
