import os

from picamera2 import Picamera2
import cv2
import requests
import time

API_URL = os.getenv("API_URL", "http://localhost:9090/devices/images")
API_KEY = os.getenv("API_KEY", "")
HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}

picam2 = Picamera2()
picam2.start()

while True:
    # Capture image as numpy array
    image = picam2.capture_array()
    _, img_encoded = cv2.imencode('.jpg', image)
    files = {'image': ('img.jpg', img_encoded.tobytes(), 'image/jpeg')}
    response = requests.post(API_URL, files=files, headers=HEADERS, timeout=10)
    time.sleep(2)
    print(f"Response: " + str(response.content, "utf-8"))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.close()