FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y pip
RUN pip install --upgrade pip

WORKDIR /backend
COPY . .

RUN mv scripts /
RUN chmod +x /scripts/*

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install


ENTRYPOINT ["/scripts/entrypoint.sh"]