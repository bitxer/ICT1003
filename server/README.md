# Server
## Installation
### Development
1. Execute the script `dev.sh` in a unix environment.
2. If you would like to make use of telegram functionality ensure that docker and the relevant go packages is installed. After which run the following command:
```
$ docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3.8-management-alpine
$ go get github.com/go-telegram-bot-api/telegram-bot-api
$ go get github.com/streadway/amqp
$ cd telegram
$ go run telegram.go
```

### Production
1. Install docker and docker-compose
2. Execute the script `deploy.sh`
