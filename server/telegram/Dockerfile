FROM golang:1.15-alpine3.12

RUN mkdir -p /opt/telegram/uploads
WORKDIR /opt/telegram
COPY telegram.go /opt/telegram/
COPY config.prod.json /opt/telegram/config.json

RUN rm -rf /var/cache/apk/* /tmp/* && \
    apk update && apk upgrade && \
    apk add git --no-cache && \
    go get github.com/go-telegram-bot-api/telegram-bot-api github.com/streadway/amqp && \
    go build -o telegram

ENTRYPOINT [ "./telegram" ]