# Live Video Streaming & Face Recognition

This project provides a live video streaming and face recognition system using FastAPI, OpenCV, dlib, and MQTT. It is designed to run on devices such as Raspberry Pi with Pi Camera support.

## Features

- Live video capture from camera
- Face detection and recognition using dlib and OpenCV
- MQTT integration for device state communication
- REST API for image upload and recognition

## Getting Started

### Prerequisites

- Python 3.11+
- MQTT broker (e.g., Mosquitto)
- Docker (optional)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jobijose/face-recognizer.git
    cd face-recognizer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

#### Run the FastAPI server

```bash
run.sh
```

#### Build Docker Image

```bash
docker build -t live-face-capture:2.0 .
```

## API Endpoints

- `POST /devices/images`  
  Upload an image for face recognition.

  When `API_KEY` is set, the request must include an `X-API-Key` header with that value.

## Configuration

All settings are read from environment variables; keep secrets out of source control.

| Variable | Default | Purpose |
| --- | --- | --- |
| `API_KEY` | _(empty, no auth)_ | Shared key required in the `X-API-Key` header for image uploads. Strongly recommended on any shared network. |
| `ALLOWED_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | Comma-separated CORS origins allowed to call the API. |
| `MAX_UPLOAD_BYTES` | `5242880` | Maximum accepted upload size. |
| `OPENCV_IO_MAX_IMAGE_PIXELS` | `16777216` | Maximum decoded image size, guards against decompression bombs. |
| `MQTT_BROKER` / `MQTT_PORT` | `localhost` / `1883` | MQTT broker address. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | _(unset)_ | MQTT credentials. |
| `MQTT_TLS` | `false` | Set to `true` to connect to the broker over TLS. |
