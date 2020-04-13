FROM python:3.8-alpine

WORKDIR /app/

ARG ENVIRONMENT="PRODUCTION"
ENV ENVIRONMENT=${ENVIRONMENT}

RUN apk add build-base
COPY ./requirements/ /app/requirements/
RUN pip install --no-cache-dir \
                $([ "$ENVIRONMENT" = "PRODUCTION" ] && echo "-r requirements/base.txt") \
                $([ "$ENVIRONMENT" = "DEVELOPMENT" ] && echo "-r requirements/dev.txt")

COPY . /app/
RUN pip install --no-deps /app/
