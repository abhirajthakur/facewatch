export interface ROI {
  id?: number;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface WebSocketResponse {
  frame?: string;
  roi?: ROI;
  error?: string;
}
