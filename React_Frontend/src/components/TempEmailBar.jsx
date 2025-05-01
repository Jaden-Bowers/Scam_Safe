// Holds the temp mail address, refresh, and copy buttons,
// and handles websocket connections

import React, { useState } from "react";

// for self hosting your going to want to make your own
// .env file and load it here
const BACKEND_WS_URL = // load backend url from .env here ie. http://ip_address:port;

function TempEmailBar({ setAnalysis }) {
  const [tempEmail, setTempEmail] = useState("Click Reload Button to Start ->");
  const [ws, setWs] = useState(null);

  const generateNewEmail = () => {
    const newEmail = `fwrd2me_${Math.floor(Math.random() * 10000)}@fwrd2me.xyz`;
    setTempEmail(newEmail);
    setAnalysis("Waiting for email analysis...");

    // handle closing prevous websocket
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("Closing previous WebSocket");
      ws.close();
    }

    const newWs = new WebSocket(`${BACKEND_WS_URL}/${newEmail}`);

    // some logging for socket connections
    newWs.onopen = () => {
      console.log("WebSocket connection opened");
    };

    newWs.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log(`WebSocket Event: ${data.event} - ${data.message}`);
        if (data.event === "analysis_result") {
          setAnalysis(data.message); // update the analysis box once recieved
        }
      } catch (err) {
        console.warn("Non-JSON WebSocket message:", event.data);
        setAnalysis(event.data);
      }
    };

    newWs.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setWs(newWs);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(tempEmail);
  };

  return (
    <div className="mb-6">
      <div className="border-dashed border-2 border-gray-500 p-4 rounded-lg flex flex-col items-center space-y-2">
        {/* Email & buttons row */}
        <div className="flex flex-wrap justify-center gap-2 sm:flex-nowrap sm:space-x-2">
          {/* Email display */}
          <div className="bg-[#303633] px-4 py-2 rounded-lg max-w-full overflow-x-auto text-base sm:text-lg font-medium">
            {tempEmail}
          </div>

          {/* Copy button */}
          <button
            onClick={handleCopy}
            className="bg-[#303633] p-2 rounded-full hover:opacity-80 active:scale-70 active:opacity-40 transition-transform duration-150"
          >
            <img src="/copy-icon.svg" alt="Copy" className="w-5 h-5" />
          </button>

          {/* Refresh button */}
          <button
            onClick={generateNewEmail}
            className="bg-[#303633] p-2 rounded-full hover:opacity-80 active:scale-70 active:opacity-40 transition-transform duration-150"
          >
            <img src="/reload-icon.svg" alt="Refresh" className="w-5 h-5" />
          </button>
        </div>

        {/* Bottom note */}
        <p className="text-base sm:text-lg text-gray-300">
          *Note you can only send one email per address
        </p>
      </div>
    </div>
  );
}

export default TempEmailBar;
