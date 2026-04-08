import os
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2
from datetime import datetime
from server_face_recognition import initialize_data_set, recognizer

app = FastAPI()

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "").split(",")
allowed_origins = [o.strip() for o in allowed_origins if o.strip()]
# When ALLOWED_ORIGINS is unset, cross-origin requests are blocked (secure default).
# Set ALLOWED_ORIGINS to a comma-separated list of trusted origins to permit CORS.

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

static_path = os.path.join("resources", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
initialize_data_set() # Initialize the dataset upon startup

@app.post("/devices/images")
async def recognize_image(image: UploadFile = File(...)):
    img = await image.read()
    # Validate magic bytes rather than trusting the user-supplied Content-Type header
    if not (img[:3] == b'\xff\xd8\xff' or                        # JPEG
            img[:8] == b'\x89PNG\r\n\x1a\n' or                   # PNG
            (img[:4] == b'RIFF' and img[8:12] == b'WEBP')):       # WebP
        raise HTTPException(status_code=400, detail="Unsupported image type")
    npimg = np.frombuffer(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid or corrupt image")
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = recognizer(gray_frame)
    return JSONResponse(content={"status": result})

@app.get("/", response_class=HTMLResponse)
async def download_page(request: Request):
    return FileResponse("static/index.html")

@app.get("/download")
async def download_file():
    file_path = "resources/ssl/ca/ca.crt"
    return FileResponse(path=file_path, filename="client.crt", media_type="application/octet-stream")
