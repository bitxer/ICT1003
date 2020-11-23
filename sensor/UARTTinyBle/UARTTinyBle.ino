//-------------------------------------------------------------------------------
//  TinyCircuits ST BLE TinyShield UART Example Sketch
//  Last Updated 2 March 2016
//
//  Reference from Ben Rose, TinyCircuits http://tinycircuits.com
//-------------------------------------------------------------------------------

#include <SPI.h>
#include <STBLE.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include <time.h>
#include "ict1003.h"

uint8_t ble_rx_buffer[21];
uint8_t ble_rx_buffer_len = 0;
uint8_t ble_connection_state = false;
int msg_id = 0;
int door_open = 0;

#define PIPE_UART_OVER_BTLE_UART_TX_TX 0


void setup()
{
  Serial.begin(9600);
  SerialMonitorInterface.begin(9600);
  pinMode(DOOR_PIN, INPUT);
  digitalWrite(DOOR_PIN, HIGH);
  BLEsetup();
  generate_new_id();
  door_open = is_open();
}

void pack_header(uint8_t *sendBuffer, int action){
  sendBuffer[0] = VER_REV;                     // Version and Revision Fields
  sendBuffer[1] = action;                      // Action Reference Field
  sendBuffer[2] = (msg_id & 0xFF000000) >> 24; // Byte 1 of message ID
  sendBuffer[3] = (msg_id & 0x00FF0000) >> 16; // Byte 2 of message ID
  sendBuffer[4] = (msg_id & 0x0000FF00) >> 8;  // Byte 3 of message ID
  sendBuffer[5] = msg_id & 0x000000FF;         // Byte 4 of message ID
  msg_id++;                                    // Increment Message ID
}

void generate_new_id(){
  srand(time(NULL) + rand());
  msg_id = rand();
}

int is_open(){
  int current = digitalRead(DOOR_PIN);
  if (current == door_open) {
    return -1;
  }
  door_open = current;
  return current;
}

void trigger(uint8_t evt){
  if (evt == SYNC){
    generate_new_id();
  }
  uint8_t sendBuffer[6];
  pack_header(sendBuffer, evt);
  lib_aci_send_data(PIPE_UART_OVER_BTLE_UART_TX_TX, (uint8_t*)sendBuffer, 6);
}

void loop() {
  aci_loop();//Process any ACI commands or events from the NRF8001- main BLE handler, must run often. Keep main loop short.
  int is_open_stat = is_open();
  
  if (is_open_stat == -1) {
    return;
  }
  
  if (!is_open_stat) {
    trigger(OPEN);
  } else {
    trigger(CLOSE);
  }
}
