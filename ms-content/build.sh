#!/bin/bash
docker build . -t ms-content:latest --no-cache
docker tag ms-content:latest harbor.sentimail.samoth.eu/sentimail/ms-content:latest
docker push harbor.sentimail.samoth.eu/sentimail/ms-content:latest