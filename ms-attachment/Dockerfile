FROM --platform=linux/amd64 python:3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY code/. .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt