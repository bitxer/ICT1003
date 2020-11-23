/*************************************************************************
 * BMA250 TinyZero Tutorial:
 * This example program will show the basic method of printing out the 
 * accelerometer values from the BMA250 to the Serial Monitor, and the
 * Serial Plotter
 * 
 * Hardware by: TinyCircuits
 * Code by: Laverena Wienclaw for TinyCircuits
 *
 * Initiated: Mon. 11/1/2018
 * Updated: Tue. 11/1/2018
 ************************************************************************/
 
#include <Wire.h>         // For I2C communication with sensor
#include "BMA250.h"       // For interfacing with the accel. sensor

// Accelerometer sensor variables for the sensor and its values
BMA250 accel_sensor;
int x, y, z;
double temp;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  Serial.print("Initializing BMA...");
  // Set up the BMA250 acccelerometer sensor
  accel_sensor.begin(BMA250_range_2g, BMA250_update_time_64ms); 
}

void loop() {
  accel_sensor.read();//This function gets new data from the acccelerometer

  // Get the acceleration values from the sensor and store them into global variables
  // (Makes reading the rest of the program easier)
  x = accel_sensor.X;
  y = accel_sensor.Y;
  z = accel_sensor.Z;
  temp = ((accel_sensor.rawTemp * 0.5) + 24.0);

  // If the BME280 is not found, nor connected correctly, these values will be produced
  // by the sensor 
  if (x == -1 && y == -1 && z == -1) {
    // Print error message to Serial Monitor
    Serial.print("ERROR! NO BMA250 DETECTED!");
  }
  
  else { // if we have correct sensor readings: 
    showSerial();                 //Print to Serial Monitor 
    showGraph(x, y, z);           //Show on Serial Plotter
  }

  // The BMA250 can only poll new sensor values every 64ms, so this delay
  // will ensure that we can continue to read values
  delay(750);
  // ***Without the delay, there would not be any sensor output*** 
}

// Prints the sensor values to the Serial Monitor (found under 'Tools')
void showSerial() {
  SerialUSB.print("X = ");
  SerialUSB.print(x);
  
  SerialUSB.print("  Y = ");
  SerialUSB.print(y);
  
  SerialUSB.print("  Z = ");
  SerialUSB.print(z);
  
  SerialUSB.print("  Temperature(C) = ");
  SerialUSB.println(temp);
}

//Plots X, Y and Z data on Serial Plotter (found under 'Tools')
void showGraph(int x, int y, int z) {
  Serial.print(x);
  Serial.print(",");

  Serial.print(y);
  Serial.print(",");

  Serial.print(z);
  Serial.print(",");
}
