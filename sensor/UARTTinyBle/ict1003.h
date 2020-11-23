//Debug output adds extra flash and memory requirements!
#ifndef BLE_DEBUG
#define BLE_DEBUG true
#endif

#if defined(ARDUINO_ARCH_AVR)
#define SerialMonitorInterface Serial
#elif defined(ARDUINO_ARCH_SAMD)
#define SerialMonitorInterface SerialUSB
#endif


#define VER_REV 0x11

#define SYNC 0x1
#define OPEN 0x2
#define CLOSE 0x4

#define MAXDATALEN 14
#define LENOFFSET 2
#define DOOR_PIN 3
