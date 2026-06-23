# EchoTTS — Minimal AI Text-to-Speech System

## Overview

EchoTTS is a minimal full-stack AI system designed to convert text into natural speech audio through a modular, production-oriented architecture.

The goal is not to replicate large-scale commercial platforms like ElevenLabs, but to demonstrate a clean, extensible AI engineering system that integrates:

* Text-to-Speech inference (CPU-first)
* Asynchronous job processing
* Full-stack web architecture
* Future-ready GPU scaling design

This project is intentionally constrained to prioritize architecture clarity over model complexity.

---

## Core Objectives

EchoTTS is designed to demonstrate the following engineering competencies:

* Full-stack system design (frontend + backend + worker separation)
* AI inference integration (TTS pipeline)
* Asynchronous job orchestration
* Storage and retrieval of generated media
* Clean deployment strategy using containerization
* Pathway from CPU local execution → GPU cloud scaling

---

## System Architecture

```text
                ┌────────────────────┐
                │    Frontend UI     │
                │   (Next.js App)    │
                └─────────┬──────────┘
                          │ HTTP
                          v
                ┌────────────────────┐
                │   Backend API      │
                │   (FastAPI)        │
                └─────────┬──────────┘
                          │
                 Job Queue (in-memory / Redis later)
                          │
                          v
                ┌────────────────────┐
                │    TTS Worker      │
                │ (Piper / Coqui)    │
                └─────────┬──────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌────────────────────┐            ┌────────────────────┐
│   Audio Storage    │            │     Database       │
│ (local / S3 later) │            │  (MongoDB Atlas)   │
└────────────────────┘            └────────────────────┘
```

---

## Key Design Principles

### 1. Separation of Concerns

Each system component is isolated:

* API handles requests
* Worker handles inference
* Storage handles persistence
* Frontend handles UX

This enables future horizontal scaling without refactoring core logic.

---

### 2. Asynchronous Execution Model

TTS generation is treated as a long-running job.

Flow:

1. User submits text
2. API creates job
3. Worker processes job asynchronously
4. Client polls job status

This avoids blocking HTTP requests and prepares the system for GPU workloads.

---

### 3. CPU-First Design

Initial implementation is optimized for CPU execution:

* Lightweight TTS model (Piper recommended)
* No dependency on GPU infrastructure
* Local execution for fast iteration

---

### 4. GPU Upgrade Path

The architecture is explicitly designed to migrate workers to GPU instances without modifying the API layer.

Future state:

* Worker container deployed on RunPod / Vast.ai
* API remains stateless
* Queue decouples compute layer

---

## MVP Features

### Core Features

* Text → Speech generation
* Job-based processing
* Audio file output
* Basic history tracking
* Simple web interface

### Non-Goals (intentionally excluded)

* Real-time streaming
* Large-scale voice cloning (initially)
* Multi-region distributed inference
* Kubernetes orchestration

---

## Suggested Tech Stack

### Frontend

* Next.js (App Router)
* TailwindCSS
* Simple fetch-based API client

### Backend

* FastAPI
* Uvicorn
* Pydantic

### AI Layer

* Piper TTS (CPU efficient)
  [https://github.com/OHF-Voice/piper1-gpl)

### Storage

* Local filesystem (`/data/audio`)

### Database

* MongoDB / MongoDB Atlas (Document-based storage tailored for flexible job metadata)
* MongoDB Motor (Async driver for Python)

---

## API Design

### POST /generate

Creates a TTS generation job.

Request:

```json
{
  "text": "Hello world",
  "voice": "default"
}
```

Response:

```json
{
  "job_id": "abc123",
  "status": "queued"
}
```

---

### GET /status/{job_id}

Returns job state and result.

Response:

```json
{
  "job_id": "abc123",
  "status": "done",
  "audio_path": "/audio/abc123.wav"
}
```

---

## Worker Design

The worker continuously processes queued jobs:

```python
while True:
    job = queue.get()

    audio = tts.generate(job.text)

    path = f"data/audio/{job.id}.wav"
    save(audio, path)

    db.update(job.id, status="done", audio_path=path)
```

This abstraction allows future migration to distributed workers.

---

## Project Structure

```text
echotts/
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   ├── workers/
│   │   └── db/
│   │
│   └── requirements.txt
│
├── data/
│   └── audio/
│
├── docker-compose.yml
└── README.md
```

---

## Scaling Roadmap

### Phase 1 — Local MVP

* CPU-based TTS
* Single machine execution
* File-based storage

### Phase 2 — Productionization

* Redis queue
* PostgreSQL database
* Dockerized services

### Phase 3 — GPU Offloading

* Worker deployed on GPU cloud provider
* API remains unchanged

### Phase 4 — Advanced Features

* Voice cloning (XTTS)
* Streaming synthesis
* Multi-user system
* Rate limiting & billing

---

## Engineering Constraints

To maintain system simplicity:

* No Kubernetes in early stages
* No real-time streaming initially
* No distributed orchestration complexity
* No model training pipeline

---

## Learning Outcomes

This project demonstrates:

* Practical AI system integration
* Backend async architecture
* Decoupled compute desig
