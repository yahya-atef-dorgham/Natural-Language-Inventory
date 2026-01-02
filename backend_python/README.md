# Natural Language Inventory Dashboard - Python Backend

Python backend for the Natural Language Inventory Dashboard using FastAPI.

## Setup

1. Install Python 3.9+ if not already installed

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the `backend_python/` directory:
```env
PORT=3001
NODE_ENV=development
DB_PATH=inventory.db
CORS_ORIGIN=http://localhost:3000
LOG_LEVEL=info

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
OPENAI_ENABLED=true
```

## Running

```bash
python src/main.py
```

Or using uvicorn directly:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 3001
```

## API Endpoints

- `POST /api/nl-queries` - Submit a natural language query
- `GET /api/nl-queries/{sessionId}` - Get query results
- `GET /api/nl-queries` - List recent sessions

## Features

- FastAPI for high-performance API
- Native SQLite support (no WASM dependencies)
- OpenAI GPT integration with Reflection Pattern
- CORS support for frontend integration
- Comprehensive logging

