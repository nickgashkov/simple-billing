FROM python:3.8-slim

WORKDIR /app/

ARG ENVIRONMENT="PRODUCTION"
ENV ENVIRONMENT=${ENVIRONMENT}

RUN apt update \
 && apt install -y curl \
 && curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate
COPY ./requirements/ /app/requirements/
RUN pip install --no-cache-dir \
                $([ "$ENVIRONMENT" = "PRODUCTION" ] && echo "-r requirements/base.txt") \
                $([ "$ENVIRONMENT" = "DEVELOPMENT" ] && echo "-r requirements/dev.txt")

COPY . /app/
RUN pip install --no-deps /app/
