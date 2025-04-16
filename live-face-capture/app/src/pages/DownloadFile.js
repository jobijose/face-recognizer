

import React from 'react';

function DownloadFile() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4 py-10">
      <h1 className="text-2xl font-semibold mb-4">Download file</h1>
      <p className="mb-6 text-center text-gray-700 max-w-md">
        To trust our development environment, please download.
      </p>
      <a
        href="/files/client.crt"
        download
        className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
      >
        Download file
      </a>
    </div>
  );
}

export default DownloadFile;
