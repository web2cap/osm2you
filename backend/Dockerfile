FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install -y libgdal-dev
    
WORKDIR /backend
COPY . .

RUN mv scripts /
RUN chmod +x /scripts/*

RUN pip install cffi
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENTRYPOINT ["/scripts/entrypoint.sh"]
