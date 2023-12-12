# syntax=docker/dockerfile:1
FROM python:3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /sentimail
COPY . /sentimail/
RUN pip install -r requirement.txt
#RUN python manage.py makemigrations
#RUN python manage.py migrate
