#!/bin/bash
docker build . -t backend:latest --no-cache
docker tag backend:latest harbor.sentimail.samoth.eu/sentimail/backend:latest
docker push harbor.sentimail.samoth.eu/sentimail/backend:latest