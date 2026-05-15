# Face-Based Image Shortlisting System

Offline, cross-platform, modular image shortlisting system using modern face detection and face recognition pipelines.

The system scans image collections, detects faces, generates embeddings, performs vector similarity search, and shortlists images containing selected persons.

The project is designed for:

- Offline operation
- Cross-platform execution
- Modular isolated components
- Docker-first development
- CPU and GPU support
- Large-scale image collections
- Future extensibility

---

# Core Features

## Reference Person Detection

The system accepts a reference image folder and automatically:

- detects faces
- extracts embeddings
- clusters distinct persons
- generates candidate identities
- allows user confirmation

---

## Bulk Image Search

The system recursively scans image collections and:

- detects faces
- generates embeddings
- searches embeddings using vector similarity
- identifies images containing selected persons
- exports shortlisted results

---

## Fully Offline

No cloud APIs.
No internet dependency during runtime.

---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Face Detection | SCRFD |
| Face Recognition | ArcFace |
| ML Framework | InsightFace |
| Runtime | ONNX Runtime |
| Vector Search | FAISS |
| Clustering | HDBSCAN |
| Image Decode | OpenCV |
| UI | PySide6 |
| Database | SQLite |
| Packaging | Docker |
| Testing | Pytest |
| Linting | Ruff |
| Formatting | Black |
| Type Checking | MyPy |

---

# Supported Platforms

| OS | Support |
|---|---|
| Ubuntu 24.04+ | Primary |
| Windows 11 | Supported |
| Windows 10 | Supported |
| macOS | Future |

---

# Runtime Modes

## CPU Mode

Uses:
- ONNX Runtime CPU
- AVX2 optimizations

Recommended for:
- laptops
- servers
- Raspberry Pi testing
- portability

---

## GPU Mode

Uses:
- NVIDIA CUDA
- ONNX Runtime GPU

Recommended for:
- large image collections
- high-throughput processing

---

# High-Level Pipeline

## Phase 1 — Reference Processing

Input:
```
reference_people/
```

Pipeline:
1. Scan images
2. Detect faces
3. Align faces
4. Generate embeddings
5. Cluster distinct persons
6. Generate preview identities
7. User confirms persons

Output:
- confirmed person identities
- reference embeddings

---

## Phase 2 — Main Image Search

Input:
```
images_root/
```

Pipeline:
1. Recursive image scan
2. Image decode
3. Face detection
4. Face alignment
5. Embedding generation
6. FAISS similarity search
7. Match filtering
8. Shortlist export

Output:
- shortlisted images
- JSON export
- CSV export
- optional copied/symlinked results

---

# Matching Strategy

The system uses:

- multiple embeddings per person
- cosine similarity
- configurable thresholds
- optional centroid embeddings

This improves robustness for:
- lighting variation
- beard changes
- side profiles
- aging
- glasses

---

# Performance Design

## Key Principles

- avoid full image processing where unnecessary
- crop only detected faces
- parallelize pipeline stages
- use vector indexing instead of brute force search

---

# Expected Inputs

## Reference Images

Examples:
```
reference_people/
├── person_1/
├── person_2/
```

OR mixed images:
```
reference_people/
├── img001.jpg
├── img002.jpg
```

---

## Main Search Images

Examples:
```
images_root/
├── events/
├── camera/
├── whatsapp/
```

Supported formats:
- JPG
- JPEG
- PNG
- WEBP
- HEIC (optional plugin)

---

# Expected Outputs

## Shortlisted Images

Example:
```
output/
├── shortlisted/
```

---

## Export Files

Example:
```
output/
├── matches.json
├── matches.csv
```

---

# Database Design

SQLite database stores:

- image metadata
- face metadata
- embeddings
- clustering results
- processing state

---

# Example Database Tables

## images

```sql
images(
    image_id,
    path,
    hash,
    processed_at
)
```

## faces

```sql
faces(
    face_id,
    image_id,
    bbox,
    embedding_path,
    confidence
)
```

## persons

```sql
persons(
    person_id,
    label,
    reference_embedding
)
```

---

# Containerization Strategy

Each major module is independently containerized.

Benefits:
- isolated dependencies
- reproducible environments
- independent testing
- easier CI/CD
- avoids system package conflicts

---

# Module Isolation Philosophy

Each module should:

- expose clean interfaces
- have isolated tests
- have isolated containers
- avoid hidden dependencies
- support standalone execution

---

# Planned Modules

| Module | Responsibility |
|---|---|
| scanner | filesystem scanning |
| decoder | image decode |
| detector | face detection |
| aligner | face alignment |
| embedder | embedding generation |
| clusterer | identity clustering |
| indexer | FAISS indexing |
| matcher | similarity matching |
| exporter | result export |
| ui | user interface |
| database | persistence |
| orchestrator | pipeline coordination |

---

# Development Requirements

## Ubuntu

Install:
- Docker
- Docker Compose
- NVIDIA Container Toolkit (optional GPU)

---

## Windows

Install:
- Docker Desktop
- WSL2 recommended
- NVIDIA CUDA drivers (optional GPU)

---

# Python Standards

Project conventions:

- Python 3.12
- PEP 8 compliant
- snake_case naming
- PascalCase classes
- Google-style docstrings

---

# Testing Strategy

## Standalone Module Tests

Each module:
- unit tests
- container tests
- integration tests

---

## Integrated Pipeline Tests

End-to-end:
- reference processing
- embedding generation
- matching
- shortlist generation

---

# Future Enhancements

- video support
- duplicate detection
- blur filtering
- face quality scoring
- distributed processing
- REST API
- web UI
- live monitoring
- incremental indexing

---

# License

TBD