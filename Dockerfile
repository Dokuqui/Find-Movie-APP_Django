FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/prod.txt /app/
RUN pip install -r prod.txt

COPY . /app

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

CMD gunicorn find_movie.wsgi:application --bind 0.0.0.0:$PORT