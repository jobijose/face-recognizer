# ESP32 Camera — Image Capture & Upload

Captures a JPEG photo every 5 seconds and POSTs it to a REST API.

## Requirements

- PlatformIO (`pip install platformio`)
- XIAO ESP32-S3 Sense

## Setup

**1. Export credentials as environment variables:**

```bash
export WIFI_SSID="your_ssid"
export WIFI_PASSWORD="your_password"
export API_ENDPOINT="http://host:port/path"
```

**2. Flash:**

```bash
pio run --target upload
```

**3. Monitor serial output:**

```bash
pio device monitor
```
