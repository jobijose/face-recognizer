import camera
import urequests
import time
from config import WIFI_SSID, WIFI_PASSWORD, API_URL, CAPTURE_INTERVAL


def init_camera():
    camera.init(0, format=camera.JPEG, framesize=camera.FRAME_VGA)
    camera.quality(30)  

def send_frame(img_bytes):
    boundary = "boundary"
    body = (
        "--" + boundary + "\r\n"
        "Content-Disposition: form-data; name=\"image\"; filename=\"img.jpg\"\r\n"
        "Content-Type: image/jpeg\r\n\r\n"
    ).encode() + img_bytes + ("\r\n--" + boundary + "--\r\n").encode()

    headers = {
        "Content-Type": "multipart/form-data; boundary=" + boundary,
        "Content-Length": str(len(body)),
    }
    response = urequests.post(API_URL, data=body, headers=headers)
    print(f"Response: {response.text}")
    response.close()

init_camera()

while True:
    img = camera.capture()
    if img:
        try:
            send_frame(img)
        except Exception as e:
            print(f"Error with exception: {e}")
    time.sleep(CAPTURE_INTERVAL)
