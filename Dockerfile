FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project metadata first
WORKDIR /app
COPY pyproject.toml README.md CHANGELOG.md ./

# Install deps (no dev)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Copy source
COPY openinspector ./openinspector
COPY docs ./docs

# Install package
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["openinspector"] 