FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

COPY . /app

RUN pip install -r requirements/prod.txt

RUN python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
