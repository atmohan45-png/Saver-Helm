#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define GAS_PIN 34

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Temperature and Gas Sensor System Initialized...");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  int gasValue = analogRead(GAS_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  Serial.print("Gas Sensor Value: ");
  Serial.println(gasValue);

  if (gasValue > 2000) {
    Serial.println("Gas Leakage Detected!");
  }

  Serial.println("----------------------------");

  delay(2000);
}
