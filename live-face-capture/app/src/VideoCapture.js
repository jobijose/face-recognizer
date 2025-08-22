import React, { useRef, useEffect } from "react";

// API endpoint from Docker ENV
const API_ENDPOINT = "https://localhost:8080/upload";

const VideoCapture = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    startCamera();
    captureFrames();
    return () => stopCamera();
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Camera access error:", error);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };

  const captureFrames = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    setInterval(() => {
      var video = videoRef.current;
      const isPortrait = video.videoHeight > video.videoWidth;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      if (isPortrait) {
        ctx.save();
        ctx.translate(canvas.width / 2, canvas.height / 2);
        ctx.drawImage(videoRef.current, -video.videoWidth / 2, - video.videoHeight/ 2, video.videoWidth, video.videoHeight);
        ctx.restore();
      } else {
        ctx.drawImage(videoRef.current, 0, 0, canvas.width , canvas.height);
      }

      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob, "frame.jpg");

        try {
          await fetch(API_ENDPOINT, { 
            method: "POST", 
            body: formData, 
            headers: {
              "Accept": "application/json", 
            }
          });
        } catch (error) {
          console.error("Error sending frame:", error);
        }
      }, "image/jpeg");
    }, 2000);
  };

  return (
    <div className="relative w-full h-screen bg-gray-900 flex items-center justify-center">
      {/* Header */}
      <header className="absolute top-0 left-0 w-full text-center py-3 bg-black/50 text-white font-semibold text-lg backdrop-blur-md">
            Video capture 
      </header>

      {/* Video Container */}
      <div className="relative w-full h-full flex items-center justify-center">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full h-auto max-h-[90vh] object-contain border-4 border-gray-700 rounded-lg shadow-lg"
        />
        <canvas ref={canvasRef} width="1280" height="720" hidden />
        {/* Recording Indicator */}
        <div className="absolute bottom-4 right-4 px-3 py-1 text-sm font-semibold bg-red-600 text-white rounded-md shadow-md animate-pulse">
          🔴 Recording...
        </div>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-0 left-0 w-full text-center py-2 text-xs text-gray-300 bg-black/50 backdrop-blur-md">
        &copy; {new Date().getFullYear()} Video capture 
      </footer>
    </div>
  );
};

export default VideoCapture;
