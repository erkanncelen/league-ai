# syntax=docker/dockerfile:1
FROM python:3.7-bullseye
# WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip setuptools wheel
RUN python -m pip install --upgrade pip  
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["gunicorn app:app"]