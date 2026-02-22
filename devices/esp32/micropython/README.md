# ESP32-CAM Image Capture

Captures JPEG frames using an ESP32-CAM and sends them to a remote HTTP API.

## Requirements

- ESP32-CAM board
- MicroPython firmware

## Setup

1. Edit `config.py` with your values:
   ```python
   WIFI_SSID = "your_wifi_ssid"
   WIFI_PASSWORD = "your_wifi_password"
   API_URL = "http://<server-ip>:9090/devices/images"
   CAPTURE_INTERVAL = 5  
   ```

2. Upload both files to the ESP32:
   ```bash
   mpremote connect /dev/ttyUSB0 cp config.py :config.py
   mpremote connect /dev/ttyUSB0 cp image_capture.py :image_capture.py
   ```

3. Run:
   ```bash
   mpremote connect /dev/ttyUSB0 run image_capture.py
   ```

> Alternatively, use Thonny to upload and run the files.
