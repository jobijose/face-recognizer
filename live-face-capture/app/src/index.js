import React from "react";
import { createRoot } from "react-dom/client"; 
import App from "./App";
import "./index.css"; // Import global styles

// Get root element
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

// Render App
root.render(<App />);

// Register Service Worker for PWA
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/service-worker.js")
      .then(() => console.log("Service Worker Registered"))
      .catch((error) => console.error("Service Worker Registration Failed", error));
  });
}
