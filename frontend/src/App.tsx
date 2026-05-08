import { useState } from "react";
import Header from "./components/Header";
import StatusBadge from "./components/StatusBadge";
import VideoPanel from "./components/VideoPanel";

import type { ROI } from "./types/roi";

import "./App.css";

function App() {
  const [roi, setRoi] = useState<ROI | null>(null);

  const [connected, setConnected] = useState(false);

  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <div className="top-bar">
          <StatusBadge connected={connected} detected={!!roi} />
        </div>

        <VideoPanel roi={roi} setRoi={setRoi} setConnected={setConnected} />
      </main>
    </div>
  );
}

export default App;
