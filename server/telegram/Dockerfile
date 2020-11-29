FROM golang:1.15-alpine3.12

WORKDIR /opt/telegram
COPY telegram.go /opt/telegram/

RUN rm -rf /var/cache/apk/* /tmp/* && \
    apk update && apk upgrade && \
    apk add git --no-cache && \
    go get github.com/go-telegram-bot-api/telegram-bot-api github.com/streadway/amqp && \
    CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o telegram

FROM alpine:latest
RUN mkdir -p /opt/telegram/uploads && \
    rm -rf /var/cache/apk/* /tmp/* && \
    apk update && apk upgrade && \
    apk --no-cache add ca-certificates
WORKDIR /opt/telegram

COPY config.prod.json /opt/telegram/config.json
COPY --from=0 /opt/telegram/telegram .

ENTRYPOINT [ "./telegram" ]