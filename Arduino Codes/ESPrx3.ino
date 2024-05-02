#include <SoftwareSerial.h>

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN D3         // Pin connected to DHT11 sensor
#define DHTTYPE DHT11     // DHT11 sensor type
#define SOIL_MOISTURE_SENSOR_PIN A0 

const char* ssid = "IQOoo";
const char* password = "12344321";
const char* server = "api.thingspeak.com";
const char* apiKey = "Y0RJW6R6IVQWCQ4M";

DHT dht(DHTPIN, DHTTYPE);
float temperature, humidity;


const int rxPin = D7; // RX pin of ESP8266, connected to TX pin of the UART device
const int txPin = D8; // TX pin of ESP8266, connected to RX pin of the UART device

SoftwareSerial uart(rxPin, txPin); // Create a SoftwareSerial object

float phValue = 0.0; // Variable to store the pH value

void setup() {
  Serial.begin(9600); // Initialize serial communication for debugging
  uart.begin(9600); // Initialize UART communication with specified baud rate
  delay(10);

  dht.begin();

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(2000);
  
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  float soilMoisture = analogRead(SOIL_MOISTURE_SENSOR_PIN);
  float soilMoisture1 = soilMoisture-400;

  Serial.print("Temperature: ");
  Serial.println(temperature);
  Serial.print("Humidity: ");
  Serial.println(humidity);
  Serial.print("Soil Moisture: ");
  Serial.println(soilMoisture1);

  
  if (uart.available() > 0) { // Check if data is available to read
    String receivedData = uart.readStringUntil('\n'); // Read the incoming data until newline character

    // Check if the received data starts with "Aph="
    if (receivedData.startsWith("pHValue=")) {
      int indexOfEquals = receivedData.indexOf('='); // Find the index of '=' character
      int indexOfCheckChar = receivedData.indexOf('p'); // Find the index of 'A' character

      if (indexOfEquals != -1 && indexOfCheckChar == 0) { // Check if '=' is found and 'A' is at the beginning
        String phString = receivedData.substring(indexOfEquals + 1); // Extract the substring after '='

        // Convert the pH value string to float
        phValue = phString.toFloat();
        
        // Debugging: print the pH value
        Serial.print("pH Value: ");
        Serial.println(phValue);
      }
    }
  }

  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(server, httpPort)) {
    Serial.println("Connection failed");
    return;
  }

  String url = "/update?api_key=";
  url += apiKey;
  url += "&field1=";
  url += String(temperature);
  url += "&field2=";
  url += String(humidity);
  url += "&field3=";
  url += String(soilMoisture1);
  url += "&field4=";
  url += String(phValue);

  Serial.print("Requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + server + "\r\n" +
               "Connection: close\r\n\r\n");
  delay(10);

  Serial.println("Data sent to ThingSpeak!");
  client.stop();
}