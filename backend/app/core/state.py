class AppState:
    latest_processed_frame: str | None = None
    latest_roi: dict | None = None


app_state = AppState()
