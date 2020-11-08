package main

import (
	"encoding/json"
	"log"
	"os"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/streadway/amqp"
)

type Configuration struct {
	Env           string
	Debug         bool
	Testing       bool
	ChannelID     int64
	TelegramToken string
}

type Detection struct {
	Image  string
	Sensor string
	Time   string
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	// Read config file
	file, err := os.Open("./config.json")
	failOnError(err, "Can't open config file")
	defer file.Close()
	decoder := json.NewDecoder(file)
	Config := Configuration{}
	err = decoder.Decode(&Config)
	failOnError(err, "Can't decode config JSON")
	log.Println("Environment:", Config.Env)

	// Setup RabbitMQ
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"alert", // name
		true,    // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")

	err = ch.Qos(
		1,     // prefetch count
		0,     // prefetch size
		false, // global
	)
	failOnError(err, "Failed to set QoS")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	//Setup Telegram
	bot, err := tgbotapi.NewBotAPI(Config.TelegramToken)
	failOnError(err, "Error when setting up telegram")

	bot.Debug = Config.Debug

	log.Printf("Authorized on account %s", bot.Self.UserName)

	// Listen and send alert
	go func() {
		for d := range msgs {
			var detection Detection
			data := d.Body
			log.Printf("Received a message: %s", string(data))
			json.Unmarshal(data, &detection)
			log.Printf("Received a message: %s", detection.Image)
			msg := tgbotapi.NewPhotoUpload(Config.ChannelID, detection.Image)
			msg.Caption = "[" + detection.Time + "] New Detection at Sensor " + detection.Sensor
			bot.Send(msg)
			d.Ack(false)
		}
	}()

	log.Printf("Waiting for alerts. To exit press CTRL+C")
	<-forever
}
