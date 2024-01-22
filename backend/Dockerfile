# syntax=docker/dockerfile:1
FROM --platform=amd64 python:3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /sentimail
COPY ./sentimail /sentimail/
RUN pip install --upgrade pip && \
    pip install -r requirement.txt && \
    chmod +x init.sh
#RUN python manage.py makemigrations
#RUN python manage.py migrate
