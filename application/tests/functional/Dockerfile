FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /application

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTEST_RUN_CONFIG True

COPY ./tests/functional/requirements.txt tests/functional/

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r tests/functional/requirements.txt --no-cache-dir

COPY ../../ .

ENTRYPOINT python -m unittest discover