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

//Debug output adds extra flash and memory requirements!
#ifndef BLE_DEBUG
#define BLE_DEBUG true
#endif

#if defined(ARDUINO_ARCH_AVR)
#define SerialMonitorInterface Serial
#elif defined(ARDUINO_ARCH_SAMD)
#define SerialMonitorInterface SerialUSB
#endif

uint8_t ble_rx_buffer[21];
uint8_t ble_rx_buffer_len = 0;
uint8_t ble_connection_state = false;
#define PIPE_UART_OVER_BTLE_UART_TX_TX 0
// DEFINITION FOR DOOR TRIGGERS.
#define VER_REV 0x17
#define ACTION_TRIGGER_SYNC 0x1
#define ACTION_TRIGGER_OPEN 0x2
#define ACTION_TRIGGER_CLOSE 0x4
#define EMPTY_BYTE 0x00
int door_pin = 3;

typedef struct
{
  // First 24bits.
  uint8_t ver_rev;
  uint8_t action;
  uint8_t rsp_len;

  // Next 24bits.
  uint8_t otp[3];

  // Next 112bits.
  uint8_t data[14];

} PACKET;

void setup()
{
  Serial.begin(9600);
  SerialMonitorInterface.begin(9600);
  pinMode(door_pin, INPUT);
  digitalWrite(door_pin, HIGH);
  BLEsetup();
}

void loop()
{
  aci_loop(); //Process any ACI commands or events from the NRF8001- main BLE handler, must run often. Keep main loop short.
  if (ble_connection_state == 1)
  {
    SerialMonitorInterface.print("connected \n");
    // For testing open, close or sync, define here.   
    char *trigger = "OPEN";

    // When door is open.
    if (!digitalRead(door_pin))
    {
      char *trigger = "OPEN";
      // char *word = "0x02";
      // int word_len = 0;
      // for (int i = 0; word[i] != '\0'; ++i)
      // {
      //   ++word_len;
      // }
      // lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len);
      // if (!lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len))
      // {
      //   SerialMonitorInterface.println(F("TX dropped!"));
      // }

      // lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len);
      // if (!lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len))
      // {
      //   SerialMonitorInterface.println(F("TX dropped!"));
      // }
    }
    // When door is close.
    else
    {
      char *trigger = "CLOSE";
      // char *word = "0x04";
      // int word_len = 0;
      // for (int i = 0; word[i] != '\0'; ++i)
      // {
      //   ++word_len;
      // }
      // lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len);
      // if (!lib_aci_send_data((uint8_t)0, (uint8_t *)word, (uint8_t)word_len))
      // {
      //   SerialMonitorInterface.println(F("TX dropped!"));
      // }
    }
    PACKET *packet;
    // Version, Revision 8 bits.
    packet->ver_rev = VER_REV;

    // Action 8 bits
    // Trigger open.
    if (strcmp(trigger, "OPEN") == 0)
    {
      packet->action = ACTION_TRIGGER_OPEN;
    }
    // Trigger close.
    else if (strcmp(trigger, "CLOSE") == 0)
    {
      packet->action = ACTION_TRIGGER_CLOSE;
    }
    // Trigger sync.
    else
    {
      packet->action = ACTION_TRIGGER_SYNC;
    }

    // Response, Length 8 bits.
    packet->rsp_len = EMPTY_BYTE;

    // OTP 24 bits.
    for (int i = 0; i < 3; i++)
    {
      packet->otp[i] = EMPTY_BYTE;
    }

    // Data 112bits.
    for (int i = 0; i < 14; i++)
    {
      packet->data[i] = EMPTY_BYTE;
    }

    // Compile all the cols into one.
    uint8_t *compile_pack = (packet->ver_rev & 0xFF);
//        ((packet->ver_rev & 0xFF) << 38) | ((packet->action & 0xFF) << 36) |
//        ((packet->rsp_len & 0xFF) << 34) | ((packet->otp[0] & 0xFF) << 32) |
//        ((packet->otp[1] & 0xFF) << 30) | ((packet->otp[2] & 0xFF) << 28) |
//        ((packet->data[0] & 0xFF) << 26) | ((packet->data[1] & 0xFF) << 24) |
//        ((packet->data[2] & 0xFF) << 22) | ((packet->data[3] & 0xFF) << 20) |
//        ((packet->data[4] & 0xFF) << 18) | ((packet->data[5] & 0xFF) << 16) |
//        ((packet->data[6] & 0xFF) << 14) | ((packet->data[7] & 0xFF) << 12) |
//        ((packet->data[8] & 0xFF) << 10) | ((packet->data[9] & 0xFF) << 8) |
//        ((packet->data[10] & 0xFF) << 6) | ((packet->data[11] & 0xFF) << 4) |
//        ((packet->data[12] & 0xFF) << 4) | ((packet->data[1] & 0xFF) << 2) |
//        (packet->data[14] & 0xFF);

    lib_aci_send_data((uint8_t)0, compile_pack, 21);
    if (!lib_aci_send_data((uint8_t)0, compile_pack, 21))
    {
      SerialMonitorInterface.println(F("TX dropped!"));
    }
  }
  delay(2000);
}
else
{
  SerialMonitorInterface.print("not connected \n");
  delay(2000);
}

//Reciving from the prehipials device
if (ble_rx_buffer_len)
{ //Check if data is available
  SerialMonitorInterface.print(ble_rx_buffer_len);
  SerialMonitorInterface.print(" : ");
  SerialMonitorInterface.println((char *)ble_rx_buffer);
  SerialMonitorInterface.println((char *)ble_rx_buffer);

  ble_rx_buffer_len = 0; //clear afer reading
}
