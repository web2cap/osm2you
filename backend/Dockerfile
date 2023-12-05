FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y pip
RUN pip install --upgrade pip

WORKDIR /backend
COPY . .

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

CMD ["gunicorn", "osm2you.wsgi:application", "--bind", "0:8000" ]