interface StatusBadgeProps {
  connected: boolean;
  detected: boolean;
}

function StatusBadge({ connected, detected }: StatusBadgeProps) {
  return (
    <div className="status-container">
      <div className="status-pill">
        <span className={`status-dot ${connected ? "online" : "offline"}`} />

        {connected ? "Connected" : "Disconnected"}
      </div>

      <div className="status-pill">
        <span className={`status-dot ${detected ? "online" : "offline"}`} />

        {detected ? "Face Detected" : "No Face Detected"}
      </div>
    </div>
  );
}

export default StatusBadge;
