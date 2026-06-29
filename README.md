# 💼 AI Portfolio Backend

A production-ready FastAPI backend leveraging **Retrieval-Augmented Generation (RAG)** with **Google Gemini** and **Qdrant Vector Database** to power an intelligent, context-aware AI Portfolio Assistant.

This backend serves as the brain for an interactive portfolio, allowing users to chat with an AI assistant that answers questions about career, experience, skills, and background using only verified information extracted from uploaded resumes.

---

## 🛠 Tech Stack & Tools

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous, type-safe Python API framework)
- **AI Models:** Google Gemini (`gemini-2.5-flash` for generation and `gemini-embedding-001` for embeddings) via the `google-genai` SDK
- **Vector Database:** [Qdrant](https://qdrant.tech/) (High-performance vector similarity search engine)
- **Document Loading & Chunking:** [LangChain](https://python.langchain.com/) (`PyPDFLoader` & `RecursiveCharacterTextSplitter`)
- **Security:** JWT (JSON Web Tokens) with HS256 encryption, password hashing via Argon2 (`pwdlib`)
- **Package Management:** [uv](https://github.com/astral-sh/uv) (Fast, modern Python packaging tool)
- **Quality Assurance:** Ruff (Linter & Formatter), Pytest (Testing framework with coverage reporting)

---

## 🏗 System Architecture

The application utilizes a Retrieval-Augmented Generation (RAG) architecture divided into two main processing pipelines:

### 1. Resume Ingestion Pipeline (Admin Only)
Used by the administrator to upload and index the resume PDF into the vector database.

```text
┌─────────────┐
│ Admin User  │
└──────┬──────┘
       │ Upload PDF (POST /admin/resume/upload)
       ▼
┌───────────────────────────┐
│ FastAPI Admin Endpoint    │
└──────┬────────────────────┘
       │ Extract text content
       ▼
┌───────────────────────────┐
│ PDF Text Extractor (PyPDF)│
└──────┬────────────────────┘
       │ Raw text
       ▼
┌───────────────────────────┐
│ Text Splitter (LangChain) │
└──────┬────────────────────┘
       │ Text chunks
       ▼
┌───────────────────────────┐
│ Gemini Embedding Service  │
└──────┬────────────────────┘
       │ Generate 768-dim vectors
       ▼
┌───────────────────────────┐
│ Qdrant Vector Database    │ (Stored with vector & payload)
└───────────────────────────┘
```

### 2. RAG Chat & Query Pipeline (Public)
Used by portfolio visitors to query information about career history, experience, and background.

```text
┌─────────────┐
│ Public User │
└──────┬──────┘
       │ 1. Ask question (POST /chat)
       ▼
┌───────────────────────────┐
│   FastAPI Chat Endpoint   │◄──────────────────────────┐
└──────┬────────────────────┘                           │
       │ 2. Embed query text                            │
       ▼                                                │
┌───────────────────────────┐                           │
│ Gemini Embedding Service  │                           │
└──────┬────────────────────┘                           │
       │ 3. Query vector                                │
       ▼                                                │
┌───────────────────────────┐                           │
│  Qdrant Vector Database   ├─► 4. Similar chunks ──────┤
└───────────────────────────┘                           │
                                                        │
┌───────────────────────────┐                           │
│    Google Gemini LLM      │◄─ 5. Prompt with context ─┘
│    (gemini-2.5-flash)     │
└──────┬────────────────────┘
       │ 6. Generated answer
       ▼
┌───────────────────────────┐
│   FastAPI Chat Endpoint   │
└──────┬────────────────────┘
       │ 7. Return JSON response
       ▼
┌─────────────┐
│ Public User │
└─────────────┘
```

---

## 📂 Project Directory Structure

```text
portfolio-ai/
├── app/
│   ├── api/                 # API Routes (V1)
│   │   └── v1/
│   │       ├── admin.py     # Resume upload (Admin auth required)
│   │       ├── auth.py      # JWT Bearer token generation
│   │       ├── chat.py      # Public RAG chat endpoint
│   │       └── health.py    # Health check route
│   ├── core/                # Core configurations & security
│   │   ├── auth.py          # FastAPI dependencies for Authentication
│   │   ├── config.py        # Settings loaded via Pydantic Settings
│   │   ├── exceptions.py    # Global exception handlers
│   │   ├── logger.py        # Structured logging configuration
│   │   └── security.py      # Password hashing, JWT token create/verify
│   ├── dependencies/        # Dependency Injection providers
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Core business logic services
│   │   ├── auth_service.py       # Handles admin authentication
│   │   ├── chat_service.py       # Handles context-retrieved chat generation
│   │   ├── chunking_service.py   # Handles text chunking using LangChain
│   │   ├── embedding_service.py  # Connects to Gemini Embeddings API
│   │   ├── gemini_service.py     # Connects to Gemini LLM Generation API
│   │   ├── prompt_service.py     # Prepares prompt templates for LLM
│   │   ├── qdrant_service.py     # Interacts with Qdrant Vector database
│   │   └── resume_service.py     # Orchestrates document upload and RAG storage
│   ├── utils/               # General utility helper files
│   │   └── pdf.py           # PyPDF text extraction wrapper
│   └── main.py              # Application entrypoint
├── tests/                   # Complete Unit and Integration tests
├── docker-compose.yml       # Docker Compose setup for Qdrant
├── pyproject.toml           # Project dependencies & configurations
├── pytest.ini               # Pytest settings
├── uv.lock                  # UV lockfile
└── README.md                # Documentation (this file)
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure the following parameters:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `APP_NAME` | The application title display name | `AI Portfolio API` |
| `APP_VERSION` | Current application API version | `1.0.0` |
| `DEBUG` | Enable or disable debug mode | `true` |
| `HOST` | Server host address | `127.0.0.1` |
| `PORT` | Server port | `8000` |
| `GOOGLE_API_KEY` | Google Gemini AI Platform API Key | *Required* |
| `GEMINI_MODEL` | Gemini LLM model to use for generation | `gemini-2.5-flash` |
| `EMBEDDING_MODEL` | Embedding model to use for vectors | `gemini-embedding-001` |
| `QDRANT_HOST` | Host address for Qdrant DB | `localhost` |
| `QDRANT_PORT` | Port for Qdrant DB | `6333` |
| `COLLECTION_NAME` | Vector collection name in Qdrant | `portfolio_resume` |
| `JWT_SECRET_KEY` | Secret key used for signing JWT tokens | *Required in Prod* |
| `JWT_ALGORITHM` | Algorithm used for JWT encoding | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration duration | `60` |
| `ADMIN_USERNAME` | Username for accessing admin endpoints | `admin` |
| `ADMIN_PASSWORD_HASH` | Hashed admin password (see Setup section below) | *Required* |

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.13+** installed.
2. **[uv](https://github.com/astral-sh/uv)** installed (recommended Python package installer).
3. **Docker Desktop** installed (to run Qdrant).

### Step-by-Step Setup

1. **Clone & Navigate:**
   ```bash
   git clone <repository-url>
   cd portfolio-ai
   ```

2. **Spin up Qdrant Database:**
   Start the Qdrant vector database container in the background:
   ```bash
   docker compose up -d
   ```

3. **Configure Environment Variables:**
   Create a copy of `.env.example` as `.env`:
   ```bash
   copy .env.example .env
   ```

4. **Generate Hashed Admin Password:**
   Admin authentication uses password hashing. Generate a hashed password using the application's built-in hashing:
   ```bash
   uv run python -c "from app.core.security import SecurityService; print(SecurityService.hash_password('your_secure_password'))"
   ```
   Copy the output hash and set it as `ADMIN_PASSWORD_HASH` in `.env`, and update `ADMIN_USERNAME` (e.g. `test` or `admin`).

5. **Install Dependencies:**
   Sync the Python virtual environment and dependencies using `uv`:
   ```bash
   uv sync
   ```

6. **Start the Backend Server:**
   Launch the FastAPI ASGI application:
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   The backend will start running on [http://localhost:8000](http://localhost:8000).

---

## 📡 API Reference & Endpoints

### 1. Health check
- **Endpoint:** `GET /health`
- **Response:**
  ```json
  {
    "status": "healthy",
    "application": "AI Portfolio API",
    "version": "1.0.0"
  }
  ```

### 2. Administrator Authentication
- **Endpoint:** `POST /auth/login`
- **Payload:**
  ```json
  {
    "username": "your_username",
    "password": "your_secure_password"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "ey...",
    "token_type": "bearer"
  }
  ```

### 3. Ingest Resume (Admin Only)
- **Endpoint:** `POST /admin/resume/upload`
- **Headers:** `Authorization: Bearer <access_token>`
- **Content-Type:** `multipart/form-data`
- **Form Data:** `file` (must be a PDF document)
- **Response:**
  ```json
  {
    "filename": "uuid-file-name.pdf",
    "original_filename": "karun_mourya_resume.pdf",
    "content_type": "application/pdf",
    "size": 128450,
    "pages": 2
  }
  ```

### 4. Chat with Portfolio AI
- **Endpoint:** `POST /chat`
- **Payload:**
  ```json
  {
    "message": "What is Karun's experience with FastAPI?"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "Karun has extensive experience building FastAPI backends. In his portfolio project, he implemented a production-ready AI backend utilizing FastAPI to handle secure PDF ingestion, JWT authentication, and structured chat interfaces..."
  }
  ```

### 🔍 Interactive API Docs
Once the server is running, you can explore the API endpoints visually:
- **Swagger UI (Interactive Console):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc (Static Documentation):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Tests & Quality Control

### Run the Test Suite
The project contains comprehensive unit tests to ensure application reliability. Run them using pytest:
```bash
uv run pytest
```

### Check Test Coverage
To generate a test coverage report:
```bash
uv run pytest --cov=app
```

### Code Quality (Linting & Formatting)
Ensure standard code formatting and syntax cleanliness rules using Ruff:
```bash
# Run the linter
uv run ruff check app tests

# Auto-format codebase
uv run ruff format app tests
```
