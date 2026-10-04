import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np

from server_face_recognition import initialize_data_set, recognizer


MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", "5242880"))
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

app = FastAPI(title="Face Recognizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

static_path = (Path("resources") / "static").resolve()
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

initialize_data_set()  # Initialize the dataset upon startup


@app.post("/devices/images")
async def recognize_image(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG, and WEBP images are allowed.")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")
    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Uploaded image exceeds the maximum allowed size.")

    npimg = np.frombuffer(image_bytes, dtype=np.uint8)
    if npimg.size == 0:
        raise HTTPException(status_code=400, detail="Uploaded image could not be decoded.")

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if frame is None or frame.size == 0:
        raise HTTPException(status_code=400, detail="Invalid image content provided.")

    result = recognizer(frame)
    return JSONResponse(content={"status": result})


@app.get("/", response_class=HTMLResponse)
async def download_page(request: Request):
    index_path = (static_path / "index.html").resolve()
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Index page not found.")
    return FileResponse(path=str(index_path))


@app.get("/download")
async def download_file():
    file_path = (Path("resources") / "ssl" / "ca" / "ca.crt").resolve()
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Certificate file not found.")
    return FileResponse(path=str(file_path), filename="client.crt", media_type="application/octet-stream")
