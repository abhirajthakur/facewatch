import { useEffect, useRef, useState } from "react";

import type { Dispatch, SetStateAction } from "react";
import type { ROI, WebSocketResponse } from "../types/roi";

const WS_URL = import.meta.env.VITE_WS_URL;

interface VideoPanelProps {
  roi: ROI | null;
  setRoi: Dispatch<SetStateAction<ROI | null>>;
  setConnected: Dispatch<SetStateAction<boolean>>;
}

function VideoPanel({ roi, setRoi, setConnected }: VideoPanelProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [processedFrame, setProcessedFrame] = useState<string | null>(null);

  useEffect(() => {
    let websocket: WebSocket;
    let interval: number;

    async function initialize() {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      websocket = new WebSocket(WS_URL);

      websocket.onopen = () => {
        setConnected(true);
      };
      websocket.onclose = () => {
        setConnected(false);
      };
      websocket.onmessage = (event: MessageEvent<string>) => {
        const data: WebSocketResponse = JSON.parse(event.data);

        if (data.roi) {
          setRoi(data.roi);
        }
        if (data.frame) {
          setProcessedFrame(data.frame);
        }
      };

      interval = window.setInterval(() => {
        if (websocket.readyState === WebSocket.OPEN && videoRef.current && canvasRef.current) {
          const video = videoRef.current;
          if (!video.videoWidth) {
            return;
          }

          const canvas = canvasRef.current;
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;

          const context = canvas.getContext("2d");
          if (!context) {
            return;
          }

          context.drawImage(video, 0, 0);

          const frame = canvas.toDataURL("image/jpeg", 0.7);

          websocket.send(
            JSON.stringify({
              frame: frame.split(",")[1],
            }),
          );
        }
      }, 120);
    }

    initialize();

    return () => {
      if (websocket) {
        websocket.close();
      }
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [setConnected, setRoi]);

  return (
    <div className="video-layout">
      <div className="video-card">
        <video ref={videoRef} autoPlay muted playsInline className="live-video" />

        {processedFrame && (
          <img
            src={`data:image/jpeg;base64,${processedFrame}`}
            alt="Processed stream"
            className="processed-overlay"
          />
        )}
        {!processedFrame && (
          <div className="video-overlay-status">Initializing AI detection...</div>
        )}

        <canvas ref={canvasRef} className="hidden" />
      </div>

      <div className="roi-card">
        <h3>ROI Detection</h3>

        {roi ? (
          <div className="roi-grid">
            <div>
              <span>X</span>
              <strong>{Math.round(roi.x)}</strong>
            </div>

            <div>
              <span>Y</span>
              <strong>{Math.round(roi.y)}</strong>
            </div>

            <div>
              <span>Width</span>
              <strong>{Math.round(roi.width)}</strong>
            </div>

            <div>
              <span>Height</span>
              <strong>{Math.round(roi.height)}</strong>
            </div>
          </div>
        ) : (
          <p className="muted">No active detections</p>
        )}
      </div>
    </div>
  );
}

export default VideoPanel;
