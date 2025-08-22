from picamera2 import Picamera2
import cv2
import requests
import time

API_URL = "http://localhost:9090/devices/images"  # Replace with your API URL

picam2 = Picamera2()
picam2.start()

while True:
    # Capture image as numpy array
    image = picam2.capture_array()
    _, img_encoded = cv2.imencode('.jpg', image)
    files = {'image': ('img.jpg', img_encoded.tobytes(), 'image/jpeg')}
    response = requests.post(API_URL, files=files)
    time.sleep(2)
    print(f"Response: " + str(response.content, "utf-8"))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.close()