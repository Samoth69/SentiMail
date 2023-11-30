# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /sentimail
#COPY requirements.txt /sentimail/
COPY . /sentimail/
#COPY ../../.env /sentimail/
RUN pip install -r requirement.txt