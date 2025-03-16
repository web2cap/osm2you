FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev curl build-essential && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

WORKDIR /backend

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN mv scripts / \
    && chmod +x /scripts/*
ENTRYPOINT ["/scripts/entrypoint.sh"]
