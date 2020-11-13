//-------------------------------------------------------------------------------
//  TinyCircuits ST BLE TinyShield UART Example Sketch
//  Last Updated 2 March 2016
//
//  Reference from Ben Rose, TinyCircuits http://tinycircuits.com
//-------------------------------------------------------------------------------


#include <SPI.h>
#include <STBLE.h>

//Debug output adds extra flash and memory requirements!
#ifndef BLE_DEBUG
#define BLE_DEBUG true
#endif

#if defined (ARDUINO_ARCH_AVR)
#define SerialMonitorInterface Serial
#elif defined(ARDUINO_ARCH_SAMD)
#define SerialMonitorInterface SerialUSB
#endif


uint8_t ble_rx_buffer[21];
uint8_t ble_rx_buffer_len = 0;
uint8_t ble_connection_state = false;
#define PIPE_UART_OVER_BTLE_UART_TX_TX 0

int door_pin = 3;

void setup() {
  Serial.begin(9600);
  SerialMonitorInterface.begin(9600);
  pinMode(door_pin, INPUT);
  digitalWrite(door_pin, HIGH);

  //while (!SerialMonitorInterface); //This line will block until a serial monitor is opened with TinyScreen+!
  BLEsetup();
}

void loop() {
  aci_loop();//Process any ACI commands or events from the NRF8001- main BLE handler, must run often. Keep main loop short.
  if (ble_connection_state == 1) {
    SerialMonitorInterface.print("connected \n");

    if (!digitalRead(door_pin))
    {
      char* word = "0x02";
      // u_int8_t word = 0x68;

      int word_len = 0;
      for (int i = 0; word[i] != '\0'; ++i) {
        ++word_len;
      }
      lib_aci_send_data((uint8_t)0, (uint8_t*)word, (uint8_t)word_len);
      if (!lib_aci_send_data((uint8_t)0, (uint8_t*)word, (uint8_t)word_len))
      {
        SerialMonitorInterface.println(F("TX dropped!"));
      }
    }
    else
    {
      char* word = "0x04";
      int word_len = 0;
      for (int i = 0; word[i] != '\0'; ++i) {
        ++word_len;
      }
      lib_aci_send_data((uint8_t)0, (uint8_t*)word, (uint8_t)word_len);
      if (!lib_aci_send_data((uint8_t)0, (uint8_t*)word, (uint8_t)word_len))
      {
        SerialMonitorInterface.println(F("TX dropped!"));
      }
    }
    delay(2000);
  }
  else {
    SerialMonitorInterface.print("not connected \n");
    delay(2000);
  }

  //Reciving from the prehipials device
  if (ble_rx_buffer_len) {//Check if data is available
    SerialMonitorInterface.print(ble_rx_buffer_len);
    SerialMonitorInterface.print(" : ");
    SerialMonitorInterface.println((char*)ble_rx_buffer);
    SerialMonitorInterface.println((char*)ble_rx_buffer);

    ble_rx_buffer_len = 0;//clear afer reading
  }
  // Send data from serial monitor
//  if (SerialMonitorInterface.available()) {//Check if serial input is available to send
//    delay(10);//should catch input
//    uint8_t sendBuffer[21];
//    uint8_t sendLength = 0;
//    while (SerialMonitorInterface.available() && sendLength < 19) {
//      sendBuffer[sendLength] = SerialMonitorInterface.read();
//      sendLength++;
//    }
//    if (SerialMonitorInterface.available()) {
//      SerialMonitorInterface.print(F("Input truncated, dropped: "));
//      if (SerialMonitorInterface.available()) {
//        SerialMonitorInterface.write(SerialMonitorInterface.read());
//      }
//    }
//    sendBuffer[sendLength] = '\0'; //Terminate string
//    sendLength++;
}
