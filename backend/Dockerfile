FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgdal-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /backend
COPY . .

RUN mv scripts / \
    && chmod +x /scripts/*

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install

ENTRYPOINT ["/scripts/entrypoint.sh"]
