import network
import time

# Config
WIFI_SSID = "YOUR_WIFI_S"
WIFI_PASSWORD = "another_password"
API_URL = "http://localhost:9090/devices/images"
CAPTURE_INTERVAL = 5

def connect_wifi():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print(f"WiFi connected: {wlan.ifconfig()}")


connect_wifi()