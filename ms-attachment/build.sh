#!/bin/bash
docker build . -t ms-attachment:latest --no-cache
docker tag ms-attachmentt:latest harbor.sentimail.samoth.eu/sentimail/ms-attachment:latest
docker push harbor.sentimail.samoth.eu/sentimail/ms-attachment:latest