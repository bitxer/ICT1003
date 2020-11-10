FROM golang:1.15-alpine3.12

RUN rm -rf /var/cache/apk/* /tmp/* && \
    apk update && apk upgrade && \
    apk add git --no-cache

RUN go get github.com/go-telegram-bot-api/telegram-bot-api
RUN go get github.com/streadway/amqp

RUN mkdir -p /opt/telegram/uploads
WORKDIR /opt/telegram

COPY telegram.go /opt/telegram/
COPY config.prod.json /opt/telegram/config.json
RUN go build -o telegram

ENTRYPOINT [ "./telegram" ]