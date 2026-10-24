import os
import secrets
from pathlib import Path

# Cap decoded image size before cv2 is imported so a small, highly compressed
# upload cannot expand into a huge in-memory frame (decompression bomb).
os.environ.setdefault("OPENCV_IO_MAX_IMAGE_PIXELS", str(4096 * 4096))

from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
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
# When set, clients must send this value in the X-API-Key header to upload images.
API_KEY = os.getenv("API_KEY", "")

app = FastAPI(title="Face Recognizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type", "X-API-Key"],
)

static_path = (Path("resources") / "static").resolve()
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

initialize_data_set()  # Initialize the dataset upon startup


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if API_KEY and not (x_api_key and secrets.compare_digest(x_api_key.encode(), API_KEY.encode())):
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


@app.post("/devices/images", dependencies=[Depends(require_api_key)])
async def recognize_image(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG, and WEBP images are allowed.")

    # Read at most one byte past the limit so oversized uploads are never fully loaded.
    image_bytes = await image.read(MAX_UPLOAD_BYTES + 1)
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")
    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Uploaded image exceeds the maximum allowed size.")

    npimg = np.frombuffer(image_bytes, dtype=np.uint8)
    if npimg.size == 0:
        raise HTTPException(status_code=400, detail="Uploaded image could not be decoded.")

    try:
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    except cv2.error:
        raise HTTPException(status_code=400, detail="Invalid image content provided.")
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
