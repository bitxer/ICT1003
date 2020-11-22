//-------------------------------------------------------------------------------
//  TinyCircuits ST BLE TinyShield UART Example Sketch
//  Last Updated 2 March 2016
//
//  Reference from Ben Rose, TinyCircuits http://tinycircuits.com
//-------------------------------------------------------------------------------

#include <SPI.h>
#include <STBLE.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include "ict1003.h"

uint8_t ble_rx_buffer[21];
uint8_t ble_rx_buffer_len = 0;
uint8_t ble_connection_state = false;
#define PIPE_UART_OVER_BTLE_UART_TX_TX 0

// DEFINITION FOR DOOR TRIGGERS.
int door_pin = 3;

void setup()
{
  Serial.begin(9600);
  SerialMonitorInterface.begin(9600);
  pinMode(door_pin, INPUT);
  digitalWrite(door_pin, HIGH);
  BLEsetup();
}

void pack_header(uint8_t *sendBuffer, int action, uint otp){
  sendBuffer[0] = VER_REV;
  sendBuffer[1] = action;
  sendBuffer[2] = 0;
  sendBuffer[3] = otp && 0xFF0000;
  sendBuffer[4] = otp && 0x00FF00;
  sendBuffer[5] = otp && 0x0000FF;
}

void pack_data(uint8_t *sendBuffer, char * data){
  sendBuffer[LENOFFSET] = strlen(data);
  for (int i = 0; i < sendBuffer[LENOFFSET]; i++) {
    sendBuffer[6+i] = *data + i;
  }
}


void loop() {
  aci_loop();//Process any ACI commands or events from the NRF8001- main BLE handler, must run often. Keep main loop short.
  if (ble_rx_buffer_len) {//Check if data is available
    SerialMonitorInterface.print(ble_rx_buffer_len);
    SerialMonitorInterface.print(" : ");
    SerialMonitorInterface.println((char*)ble_rx_buffer);
    ble_rx_buffer_len = 0;//clear afer reading
  }
  if (SerialMonitorInterface.available()) {//Check if serial input is available to send
    delay(10);//should catch input

    uint8_t sendBuffer[21];
    char action = SerialMonitorInterface.read();
    switch (action){
      case 'o':
        pack_header(sendBuffer, OPEN, 0x0);
        break;
      case 'c':
        pack_header(sendBuffer, CLOSE, 0x0);
        break;
      default:
        return;
    }
    
    if (!lib_aci_send_data(PIPE_UART_OVER_BTLE_UART_TX_TX, (uint8_t*)sendBuffer, sendBuffer[LENOFFSET]+6))
    {
      SerialMonitorInterface.println(F("TX dropped!"));
    }
  }
}
