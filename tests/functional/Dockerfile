FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TEST_RUN_CONFIG True

EXPOSE 5432:5432
EXPOSE 6379:6379

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY . /usr/src/app/
#COPY ../../waiter.sh .
#RUN apt update && apt install -y netcat && chmod +x waiter.sh

ENTRYPOINT pytest --disable-pytest-warnings src
