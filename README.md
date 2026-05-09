# FaceWatch

Real-time face detection and ROI (Region of Interest) streaming platform built with FastAPI, React, WebSockets, PostgreSQL, Docker, and dlib.

FaceWatch captures live webcam frames from the browser, streams them to a FastAPI backend over WebSockets, performs face detection in real-time, stores ROI metadata in PostgreSQL, draws bounding boxes without OpenCV, and streams processed frames back to the frontend.

# Features

- Real-time webcam streaming
- Face detection using dlib
- ROI (Region of Interest) bounding box rendering without OpenCV
- WebSocket-based low-latency communication
- Dockerized full-stack architecture
- Automatic Alembic migrations on container startup
- Environment-based configuration

# Tech Stack

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- dlib
- Pillow
- uv
- WebSockets

## Frontend

- React
- TypeScript
- Vite

## Infrastructure

- Docker
- Docker Compose
- Nginx

# Architecture

```text
    ┌──────────────┐
    │   Browser    │
    │ React + TS   │
    └──────┬───────┘
           │
           │ (1) webcam frames via WebSocket
           ▼
┌──────────────────────────┐
│      FastAPI Backend     │
│  WebSocket + REST APIs   │
└──────────┬───────────────┘
           │
           │ (2) decode JPEG frames
           ▼
┌──────────────────────────┐
│   Face Detection Layer   │
│   dlib + Pillow Drawing  │
└──────────┬───────────────┘
           │
           │ (3) persist ROI metadata
           ▼
┌──────────────────────────┐
│       PostgreSQL         │
│      ROI Persistence     │
└──────────┬───────────────┘
           │
           │ (4) latest ROI/frame retrieval
           ▼
┌──────────────────────────┐
│      REST Endpoints:     │
│     /api/frame/process   │
│     /api/video/latest    │
│     /api/roi/latest      │
└──────────────────────────┘


Containerized Deployment

┌──────────────────────────────────────────────────────┐
│                   Docker Compose                     │
│                                                      │
│  ┌─────────────┐   ┌─────────────┐   ┌────────────┐  │
│  │  Frontend   │   │   Backend   │   │ PostgreSQL │  │
│  │    Nginx    │   │   FastAPI   │   │     DB     │  │
│  └─────────────┘   └─────────────┘   └────────────┘  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

# API Endpoints

## WebSocket

### `WS /ws/video`

Primary real-time streaming endpoint.

Accepts:

- live webcam frames

Returns:

- processed frame
- ROI metadata

## REST Endpoints

### `POST /api/frame/process`

Accepts a single image frame upload and returns:

- processed frame
- ROI metadata

This endpoint exists to satisfy the explicit API ingestion requirement independently from the WebSocket transport layer.

### `GET /api/video/latest`

Returns the latest processed video frame.

### `GET /api/roi/latest`

Returns the latest detected ROI metadata.

### `GET /health`

Health check endpoint.

# Project Structure

```text
facewatch/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```


# Getting Started

## Run with Docker

### Prerequisites

- Docker
- Docker Compose

### Run the Application

```bash
DOCKER_BUILDKIT=1 docker-compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

## Environment Variables

### Backend

```env
DEBUG=true
FRONTEND_URL=http://localhost:5173
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/facewatch
SYNC_DATABASE_URL=postgresql://postgres:postgres@postgres:5432/facewatch
```

## Run Without Docker

### Prerequisites

- Python 3.11
- PostgreSQL
- uv
- Node.js 20+

## Backend Setup

### Navigate to Backend

```bash
cd backend
```

### Install Dependencies

```bash
uv sync
```

### Configure Environment Variables

Create:

```text
backend/.env
```

```env
DEBUG=true
FRONTEND_URL=http://localhost:5173
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/facewatch
SYNC_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/facewatch
```

### Run Database Migrations

```bash
uv run alembic upgrade head
```

### Start Backend Server

```bash
uv run uvicorn app.main:app --reload
```

Backend will run on:

```text
http://localhost:8000
```

## Frontend Setup

### Navigate to Frontend

```bash
cd frontend
```

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Create:

```text
frontend/.env
```

```env
VITE_WS_URL=ws://localhost:8000/ws/video
```

### Start Frontend

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```


# Design Decisions

## Why dlib?

dlib provides:

- lightweight face detection
- CPU-only inference
- easy containerization
- no OpenCV dependency

## Why Pillow Instead of OpenCV?

The assignment explicitly prohibited OpenCV.

Pillow was used to:

- render bounding boxes
- manipulate image frames
- encode/decode JPEG frames

without introducing unnecessary complexity.

# Expectations / Notes

## dlib Build Time

The first Docker build may take several minutes because:

- dlib contains native C++ extensions
- compilation occurs during dependency installation

Subsequent builds are significantly faster due to Docker layer caching.

## Webcam Permissions

The browser will request webcam access permission when the frontend loads.
The application will not function correctly unless webcam access is granted.

## Lighting Conditions

The dlib frontal face detector performs best under:

- reasonable lighting
- frontal face orientation
- moderate image contrast

Very poor lighting conditions may reduce detection reliability.

# Database Migrations

Alembic migrations run automatically during backend container startup.

No manual migration step is required.

# AI Usage Disclosure

AI-assisted development tools were used during implementation for:

- architecture planning
- debugging assistance
- Docker optimization
- frontend structure guidance
- documentation refinement

All generated code was manually reviewed, modified, tested, and integrated into the final solution.
