FROM golang:1.15-alpine3.12

RUN go get github.com/go-telegram-bot-api/telegram-bot-api
RUN go get github.com/streadway/amqp

RUN mkdir -p /opt/telegram/uploads
WORKDIR /opt/telegram

COPY telegram.go /opt/telegram/
COPY config.json /opt/telegram/