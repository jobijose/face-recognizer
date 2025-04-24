import os
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2
from datetime import datetime
from server_face_recognition import initialize_data_set, recognizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = os.path.join("resources", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.post("/devices/images")
async def recognize_image(image: UploadFile = File(...)):
    img = await image.read()
    npimg = np.frombuffer(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = recognizer(gray_frame)
    return JSONResponse(content={"status": result})

@app.get("/", response_class=HTMLResponse)
async def download_page(request: Request):
    return FileResponse("static/index.html")

@app.get("/download")
async def download_file():
    file_path = "resources/ssl/client.crt"
    return FileResponse(path=file_path, filename="client.crt", media_type="application/octet-stream")

if __name__ == "__main__":
    initialize_data_set()
