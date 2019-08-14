FROM python:3.6-alpine AS base
MAINTAINER Chirag Maliwal "chiragmaliwal1995@gmail.com"

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build
COPY . /src
WORKDIR /src
CMD  ["python", "app.py"]