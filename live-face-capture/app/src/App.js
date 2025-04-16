import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VideoCapture from "./VideoCapture";
import DownloadFile from './pages/DownloadFile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VideoCapture />} />
        <Route path="/download" element={<DownloadFile />} />
      </Routes>
    </Router>
  );
}

export default App;

