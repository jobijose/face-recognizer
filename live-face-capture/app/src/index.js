import React from "react";
import { createRoot } from "react-dom/client"; 
import App from "./App";
import "./index.css"; // Import global styles
import * as serviceWorkerRegistration from './serviceWorkerRegistration';

// Get root element
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

// Render App
root.render(<App />);

serviceWorkerRegistration.register(); 