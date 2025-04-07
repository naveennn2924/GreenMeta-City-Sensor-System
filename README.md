# GreenMeta City – Smart City Sensor System

This project was developed during the GreenMeta City Sustainable Design Challenge (EELISA 4th Joint Call).  
Our team worked on the **Sensor Data Integration** module using the ESP32-WROOM-32 board.

## Features
- Real-time temperature & humidity monitoring with DHT11
- Data pushed every 2 seconds via HTTP POST (after MQTT failed due to SSL issues)
- Live chart visualization (like stock market chart)
- HTML/CSS interface displaying current sensor data
- Smart Home simulation:
  - PIR motion sensor triggers buzzer + RGB LED
  - RFID-based servo door lock system

## Components Used
- ESP32-WROOM-32
- DHT11 Sensor
- PIR Sensor
- RGB LED
- Buzzer
- RFID RC522
- Servo Motor

## Scripts
- `Arduino/..` – Arduino sketch
- `Interface/websocket.py` – Python HTTP receiver

## Team
- Sensor Data Team – GreenMeta City
- In collaboration with Unity modeling and strategy teams

## License
MIT