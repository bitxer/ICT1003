int door_pin = 3;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(door_pin,INPUT);
  digitalWrite(door_pin,HIGH);
  Serial.println(("Initializing..."));
}

void loop() {
  // put your main code here, to run repeatedly:

   if (!digitalRead(door_pin))
        {
          SerialUSB.println("OPEN!");
        }
        else
        {
          SerialUSB.println("CLOSED!");
        }
   delay(1000);
}
