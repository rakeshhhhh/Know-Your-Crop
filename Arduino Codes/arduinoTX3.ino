#include <SoftwareSerial.h>
#include <stdio.h>

#define SensorPin A0          // the pH meter Analog output is connected with the Arduino’s Analog
unsigned long int avgValue;  //Store the average value of the sensor feedback
float b;
float sensordata;
int buf[10],temp;

// Define the software serial pins
#define TX_PIN 2
#define RX_PIN 3

// Create a SoftwareSerial object
SoftwareSerial mySerial(TX_PIN, RX_PIN);

void setup() {
  pinMode(13, OUTPUT);
  // Initialize serial communication at 9600 baud for both hardware and software serial
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  sensordata = analogRead(SensorPin);

  for(int i = 0; i < 10; i++) {
    buf[i] = analogRead(SensorPin);
    delay(10);
  }
  for(int i = 0; i < 9; i++) {
    for(int j = i + 1; j < 10; j++) {
      if(buf[i] > buf[j]) {
        temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }
  avgValue = 0;
  for(int i = 2; i < 8; i++) {
    avgValue += buf[i];
  }
  float aph = (float)avgValue * 5.0 / 1024 / 8.1;
  aph = 3.5 * aph;
  // Serial.println(phValue, 2);
  float pht = 7.25;
  if(aph > pht){
    aph= aph-1.65;
  }
  
  delay(1000);
  // Transmit a string

  char buffer[20]; // Buffer to store the formatted string
  char buffer2[20]; // Buffer to store the formatted string

  dtostrf(aph, 5, 2, buffer); // 5 is minimum width, 2 is precision

  // Concatenate units and label
  sprintf(buffer2, "pHValue=%s", buffer);
  mySerial.println(buffer2); // Send the string over software serial
  
  // Print a message to the hardware serial monitor
  Serial.println(buffer2);
  
  // Delay for 1 second
  delay(1000);
}
