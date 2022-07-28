FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5432:5432
EXPOSE 6379:6379

WORKDIR /usr/src/application
# TODO: доделать
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY . /usr/src/app/

ENTRYPOINT python utils/wait_for.py && pytest --disable-pytest-warnings src
