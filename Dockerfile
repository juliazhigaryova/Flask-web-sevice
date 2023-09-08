FROM python:3.7-slim

COPY . /backend
WORKDIR /backend
COPY requirements.txt /backend
RUN pip install -r requirements.txt