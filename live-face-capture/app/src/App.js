import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VideoCapture from "./VideoCapture";
import DownloadFile from './pages/DownloadFile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VideoCapture />} />
      </Routes>
    </Router>
  );
}

export default App;

