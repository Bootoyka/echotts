# EchoTTS

> A production-inspired Text-to-Speech inference service built to demonstrate modern AI/ML engineering practices.

## Overview

EchoTTS is a backend-focused AI application that converts text into speech through an asynchronous inference pipeline.

The objective is not to compete with commercial TTS platforms such as ElevenLabs, but to showcase the engineering practices behind deploying machine learning models as production-ready services.

The project emphasizes:

* asynchronous job processing
* service-oriented architecture
* containerized deployment
* clean separation between API and inference
* reproducible local development
* extensibility for future models and GPU inference

---

# Features

## Implemented

* Text-to-Speech generation using Piper
* Asynchronous job processing
* Redis-backed job queue
* MongoDB job persistence
* Dedicated worker process
* REST API with FastAPI
* Docker Compose deployment
* Shared audio storage
* Job status tracking
* Environment-based configuration

## Planned

* Frontend web interface
* Audio download endpoint
* Request validation improvements
* Health checks
* Metrics and monitoring
* CI/CD with GitHub Actions
* Support for additional TTS models (XTTS, StyleTTS2)

---

# Architecture

```text
                  Client
                     │
              HTTP Request
                     │
                     ▼
             ┌──────────────┐
             │  FastAPI API │
             └──────┬───────┘
                    │
          Save Job  │  Enqueue Job
                    ▼
             ┌──────────────┐
             │   MongoDB    │
             └──────────────┘
                    ▲
                    │
             ┌──────────────┐
             │    Redis     │
             └──────┬───────┘
                    │
              Dequeue Job
                    ▼
             ┌──────────────┐
             │    Worker    │
             └──────┬───────┘
                    │
            Piper Inference
                    │
                    ▼
           Generated WAV File
```

The API never performs inference directly.

Instead, it stores the job, publishes its identifier to Redis, and immediately returns control to the client.

The worker independently consumes queued jobs, performs speech synthesis, updates MongoDB, and writes the generated audio to shared storage.

This architecture allows the API layer to remain stateless while inference can scale independently.

---

# Technology Stack

| Layer            | Technology           |
| ---------------- | -------------------- |
| API              | FastAPI              |
| Worker           | Python               |
| Validation       | Pydantic             |
| Queue            | Redis                |
| Database         | MongoDB              |
| TTS Engine       | Piper                |
| Containerization | Docker Compose       |
| Audio Storage    | Shared Docker volume |

---

# Project Structure

```text
echotts/
│
├── backend/
│   ├── app/
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   └── requirements/
│
├── data/
│   └── audio/
│
├── models/
│   └── piper/
│
├── docker-compose.yml
│
└── README.md
```

---

# Getting Started

## Requirements

* Docker
* Docker Compose v2

Clone the repository:

```bash
git clone https://github.com/Bootoyka/echotts.git
cd echotts
```

Create the environment file:

```bash
cp backend/.env.example backend/.env
```

Start every service:

```bash
docker compose up --build
```

The application starts the following services:

* FastAPI API
* Worker
* Redis
* MongoDB

---

# API

## Generate Speech

```http
POST /generate
```

Request

```json
{
    "text": "Hello world",
    "voice": "default"
}
```

Response

```json
{
    "job_id": "...",
    "status": "queued"
}
```

---

## Check Job Status

```http
GET /status/{job_id}
```

Example response

```json
{
    "job_id": "...",
    "status": "done",
    "audio_url": "/audio/...",
    "created_at": "...",
    "started_at": "...",
    "completed_at": "..."
}
```

---

# Processing Pipeline

```text
POST /generate
        │
        ▼
Store job in MongoDB
        │
        ▼
Publish job ID to Redis
        │
        ▼
Worker consumes queue
        │
        ▼
Run Piper inference
        │
        ▼
Write audio file
        │
        ▼
Update MongoDB
        │
        ▼
Client polls /status/{job_id}
```

---

# Design Principles

## Asynchronous Processing

Speech synthesis is treated as a background task rather than an HTTP request.

This prevents inference latency from blocking the API and enables horizontal scaling through additional worker instances.

---

## Separation of Responsibilities

Each component has a single responsibility.

* API receives requests.
* Redis coordinates work.
* Worker performs inference.
* MongoDB stores metadata.
* Shared storage contains generated audio.

This keeps the system modular and simplifies future evolution.

---

## Model Agnostic Design

Although Piper is currently used for inference, the worker architecture is intentionally isolated from the API.

Replacing Piper with another engine (XTTS, StyleTTS2, or a proprietary model) requires changes only inside the worker layer.

---

# Roadmap

## Milestone 1 — MVP

* [x] FastAPI backend
* [x] Job persistence
* [x] Redis queue
* [x] Worker process
* [x] Piper integration
* [x] Docker Compose deployment

## Milestone 2 — Production Readiness

* [ ] Audio download endpoint
* [ ] Improved logging
* [ ] Health checks
* [ ] Automated tests
* [ ] CI/CD pipeline
* [ ] Metrics

## Milestone 3 — ML Engineering

* [ ] Multiple TTS models
* [ ] Model selection
* [ ] Batch inference
* [ ] Performance benchmarking
* [ ] GPU worker support

---

# Why This Project?

EchoTTS was built as a portfolio project to demonstrate the engineering required to deploy machine learning models in a production-inspired environment.

Rather than focusing solely on model quality, the project emphasizes system design, reproducibility, service separation, asynchronous processing, and deployment—skills commonly expected of Machine Learning Engineers and AI Engineers.

---

# License

MIT License.
