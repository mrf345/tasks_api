FROM python:3.8-alpine
RUN apk update
RUN apk add --no-cache \
    gcc \
    python3-dev \
    libc-dev \
    mariadb-connector-c-dev	\
    && rm -rf /var/cache/apk/*
RUN mkdir /app && chmod 777 /app
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
