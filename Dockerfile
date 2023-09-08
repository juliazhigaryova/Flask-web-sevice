FROM python:3.7-slim

COPY . /backend
WORKDIR /backend
RUN pip install flask gunicorn