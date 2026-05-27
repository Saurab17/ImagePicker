# FaceMatch

Offline, modular, cross-platform face-based image shortlisting system.

FaceMatch scans large image collections, detects faces, clusters identities from reference images, performs vector similarity search, and exports shortlisted results containing selected persons.

Designed for:
- Offline execution
- Cross-platform deployment
- Modular ML pipelines
- API-driven architecture
- CPU and GPU runtimes
- Large-scale image collections
- Future distributed execution

---

## Project Status

⚠️ FaceMatch is currently under active architecture and infrastructure development.

The project is presently focused on:
- Core pipeline contracts
- Shared schemas/interfaces
- Resource-aware orchestration
- Persistent task architecture
- Cross-platform build infrastructure

Implementation roadmap is phase-driven.

---

# Core Features

- Offline face-based image search
- Persistent reusable identity database
- Resumable long-running tasks
- Pluggable ML backends
- API-first architecture
- CPU/GPU runtime support
- Desktop, Android, and web client support
- Low-copy / shared-memory-oriented pipeline design
- Containerized development workflow

---

# High-Level Architecture

```text
Clients
   │
   ▼
API Layer
   │
   ▼
Task Manager
   │
   ▼
Orchestrator
   │
   ▼
Pipeline Modules
   │
   ├── Scanner
   ├── Decoder
   ├── Detector
   ├── Aligner
   ├── Embedder
   ├── Clusterer
   ├── Indexer
   ├── Matcher
   └── Exporter
   │
   ▼
Database + Vector Index + Shared Memory
```

---

# Main Processing Pipeline

```text
Filesystem Images
        │
        ▼
    Scanner
        │
        ▼
    Decoder
        │
        ▼
    Detector
        │
        ▼
    Aligner
        │
        ▼
    Embedder
        │
        ▼
     Indexer
        │
        ▼
     Matcher
        │
        ▼
     Exporter
        │
        ▼
  Shortlisted Results
```

---

# Reference Identity Workflow

```text
Reference Images
        │
        ▼
    Detection
        │
        ▼
   Embeddings
        │
        ▼
   Clustering
        │
        ▼
Identity Review UI
        │
        ▼
 Persistent Identity Database
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Runtime | ONNX Runtime |
| Detection | SCRFD |
| Recognition | ArcFace |
| Vector Search | FAISS |
| Clustering | HDBSCAN |
| API | FastAPI |
| Desktop UI | PySide6 |
| Database | SQLite |
| Packaging | Docker + PyInstaller |
| Testing | PyTest |
| Linting | Ruff |
| Formatting | Black |
| Typing | MyPy |

---

# Project Structure

```text
project/
├── backend/
├── clients/
├── configs/
├── docker/
├── models/
├── data/
├── scripts/
├── tests/
├── benchmarks/
├── packaging/
└── docs/
```

---

# Supported Platforms

| Platform | Status |
|---|---|
| Linux | Planned |
| Windows | Planned |
| Android | Planned |
| Web | Planned |
| macOS | Future |

---

# Architecture Principles

- Modular isolated components
- Stable interfaces/contracts
- API-first communication
- Shared-memory-oriented processing
- Resource-aware execution
- Cross-platform portability
- Swappable ML backends
- Persistent resumable operations

---

# Planned Runtime Support

- CPU execution
- CUDA acceleration
- TensorRT acceleration
- Future mobile runtimes

---

# Development Roadmap

| Phase | Status |
|---|---|
| Foundation & Infrastructure | In Progress |
| Scanner | Planned |
| Decoder | Planned |
| Detector | Planned |
| Aligner | Planned |
| Embedder | Planned |
| Database | Planned |
| Task Manager | Planned |
| Clusterer | Planned |
| Indexer | Planned |
| Matcher | Planned |
| Exporter | Planned |
| API Layer | Planned |
| Client Applications | Planned |

---

# Getting Started

## Development Setup

TBD after foundational infrastructure phases are completed.

Planned setup areas:
- bootstrap scripts
- dependency installation
- model downloads
- development containers
- CI workflows

---

## Running FaceMatch

TBD after orchestrator and API phases are completed.

Planned runtime modes:
- Desktop application
- API server
- Docker deployment
- GPU runtime
- CPU runtime

---

## Build & Packaging

TBD after packaging/build pipeline phases are completed.

Planned outputs:
- Windows installers
- Linux AppImages
- Android APKs
- Docker images

---

# CI/CD

Planned GitHub Actions workflows:
- automated testing
- Docker builds
- Linux builds
- Windows builds
- Android builds
- artifact publishing

---

# Future Expansion Areas

- Video support
- Distributed execution
- Incremental indexing
- TensorRT optimization
- Remote worker nodes
- Live monitoring
- Native mobile runtimes

---

# License

TBD