FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

COPY . /app
COPY requirements/prod.txt /app/
RUN pip install -r requirements/prod.txt

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD gunicorn find_movie.wsgi:application --bind 0.0.0.0:8000
