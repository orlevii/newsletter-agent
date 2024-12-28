ARG BASE_IMAGE=python:3.12-slim
ARG POETRY_VERSION="1.8.5"

FROM $BASE_IMAGE AS builder

ARG POETRY_VERSION

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    poetry install --no-root --only=main

FROM $BASE_IMAGE
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY pyproject.toml poetry.lock ./
COPY src src
RUN . /opt/venv/bin/activate && \
    pip install --no-deps -e .

WORKDIR /data
ENTRYPOINT ["python", "-m", "newsletter_agent.main"]
