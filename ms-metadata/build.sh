#!/bin/bash
docker build . -t ms-metadata:latest --no-cache
docker tag ms-metadata:latest harbor.sentimail.samoth.eu/sentimail/ms-metadata:latest
docker push harbor.sentimail.samoth.eu/sentimail/ms-metadata:latest