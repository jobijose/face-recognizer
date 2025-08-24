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

