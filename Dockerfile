FROM python:3.13-slim

ENV PATH="/etc/poetry/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/auth-service/src"

WORKDIR /auth-service

RUN apt-get update && apt-get install -y build-essential postgresql-client \
    && rm -rf /var/lib/apt/lists/

RUN python3 -m pip install --upgrade pip \
    && pip install poetry==2.2.1
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock* /auth-service/
RUN poetry install --no-interaction --no-root

COPY . /auth-service
