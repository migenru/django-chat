FROM python:3.8.1-slim-buster

RUN useradd django

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*


# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN chown django:django /app

COPY --chown=django:django . .

USER django

RUN python manage.py collectstatic --noinput --clear


CMD set -xe; python manage.py migrate --noinput; python manage.py runserver 0.0.0.0:8000