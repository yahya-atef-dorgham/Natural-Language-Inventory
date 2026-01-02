# Natural Language Inventory Dashboard

A web application that allows users to query inventory data using natural language, with automatic translation to SQL queries using **OpenAI GPT** and the **Reflection Pattern** (draft → self-review → finalize).

## Features

- **🤖 AI-Powered Queries**: OpenAI GPT converts natural language to SQL intelligently
- **🔄 Reflection Pattern**: 3-step process (Draft → Critique → Finalize) ensures accurate, safe queries
- **📊 Data Visualization**: View results as tables and charts
- **🔒 Security First**: Built-in SQL injection prevention and query validation
- **⚡ Smart Fallback**: Automatically falls back to keyword-based generation if GPT is unavailable

## Tech Stack

- **Backend**: Python, FastAPI, SQLite (native), OpenAI GPT
- **Frontend**: TypeScript, React, Vite, Recharts
- **Testing**: Jest, Vitest, Supertest, React Testing Library
- **AI/ML**: OpenAI GPT-4o-mini for natural language processing

## Prerequisites

- Python 3.9+ and pip
- Node.js 18+ and npm (for frontend)
- Git
- **OpenAI API Key** (get one at https://platform.openai.com/api-keys)

## Setup

### 1. Clone and Install Dependencies

```bash
# Install Python backend dependencies
cd backend_python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Configure OpenAI API Key

**IMPORTANT:** The app requires an OpenAI API key for intelligent query generation.

Create a `.env` file in the `backend_python/` directory:

```env
# Server Configuration
PORT=3001
NODE_ENV=development

# Database Configuration
DB_PATH=inventory.db

# CORS Configuration
CORS_ORIGIN=http://localhost:3000

# Logging Configuration
LOG_LEVEL=info

# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_ENABLED=true
```

**Get your API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key and paste it into `.env`

**Cost:** Using `gpt-4o-mini`, each query costs ~$0.0001-0.0003. Very affordable!

💡 **No API key?** The app will automatically fall back to keyword-based query generation.

### 3. Run the Application

#### Option A: Docker Deployment (Recommended)

**Prerequisites:** Docker Desktop installed and running

**Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Manual:**
```bash
docker-compose up -d
```

Services will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:3001
- Database: localhost:5432

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

#### Option B: Local Development

**Backend (Python):**
```bash
cd backend_python
venv\Scripts\activate  # On Linux/Mac: source venv/bin/activate
python src/main.py
```

The backend will automatically create `inventory.db` with sample data on first run.

**Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

## Testing

### Backend Tests

```bash
cd backend_python
# Tests coming soon (pytest)
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── api/          # HTTP endpoints and routing
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── config/       # Configuration
│   └── tests/           # Test files
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API client
│   └── tests/           # Test files
└── specs/               # Feature specifications
```

## Usage

1. Open the dashboard in your browser (http://localhost:3000)
2. Enter a natural language query, such as:
   - "Show me top-selling products in electronics with low stock"
   - "List items that need reordering"
   - "Show me products with low stock in the last 30 days"
3. Click "Submit Query"
4. View results in the table and chart visualizations

## Development

### Building for Production

**Backend:**
```bash
cd backend_python
venv\Scripts\activate  # On Linux/Mac: source venv/bin/activate
python src/main.py
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

## License

ISC

