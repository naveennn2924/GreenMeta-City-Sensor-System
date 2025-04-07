#include <WiFi.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WebServer.h>  // Built-in for web server

// WiFi credentials
const char* ssid = "d.hip_guest";
const char* password = "digitaltwin";

// DHT sensor setup
#define DHTPIN 17
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// LCD setup (optional)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Web server runs on port 80
WebServer server(80);

float temperature = 0;
float humidity = 0;

void handleRoot() {
  String html = "<html><head><title>ESP32 DHT11</title></head><body>";
  html += "<h1>Temperature and Humidity</h1>";
  html += "<p>Temperature: " + String(temperature) + " &deg;C</p>";
  html += "<p>Humidity: " + String(humidity) + " %</p>";
  html += "</body></html>";

  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  Wire.begin(21, 22); // I2C pins
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Connecting...");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi Connected");
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());

  // Start web server
  server.on("/", handleRoot);
  server.begin();
  Serial.println("Web server started.");
}

void loop() {
  // Read sensor
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  // Update LCD
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C   ");

  lcd.setCursor(0, 1);
  lcd.print("Humidity: ");
  lcd.print(humidity);
  lcd.print(" %   ");

  server.handleClient();
  delay(1000);  // Update every 1 sec
}
