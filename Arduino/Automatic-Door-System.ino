#include <Wire.h>
#include <ESP32Servo.h>
#include "MFRC522_I2C.h"

// Pins and definitions
#define RFID_ADDR 0x28
#define servoPin 13
#define ledPin 19  // LED pin

Servo myservo;
MFRC522_I2C mfrc522(RFID_ADDR, 0xFF, &Wire);  // 0xFF = no reset pin

String password = "";

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize RFID
  mfrc522.PCD_Init();
  ShowReaderDetails();

  // Initialize Servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50);
  myservo.attach(servoPin, 1000, 2000);
  myservo.write(0);  // Door initially closed

  // Initialize LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);  // LED off initially

  Serial.println("Ready. Scan your RFID card...");
}

void loop() {
  password = "";

  // Wait for new card
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // Read UID and convert to string
  Serial.print("Card UID:");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i]);
    password += String(mfrc522.uid.uidByte[i]);
  }
  Serial.println();

  // Match UID
  if (password == "12214848181") {
    Serial.println("Access granted - opening door");
    myservo.write(180);       // Open door
    digitalWrite(ledPin, HIGH); // Turn LED ON
    delay(4000);              // Keep door open 8 seconds
    Serial.println("Auto-closing door");
    myservo.write(0);         // Close door
    digitalWrite(ledPin, LOW);  // Turn LED OFF
  } else {
    Serial.println("Access denied");
  }

  delay(1000);  // Prevent rapid re-reading
}

void ShowReaderDetails() {
  byte v = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  Serial.print("MFRC522 Version: 0x");
  Serial.print(v, HEX);
  if (v == 0x91) Serial.println(" = v1.0");
  else if (v == 0x92) Serial.println(" = v2.0");
  else Serial.println(" (unknown)");

  if (v == 0x00 || v == 0xFF) {
    Serial.println("WARNING: RFID not connected properly!");
  }
}
