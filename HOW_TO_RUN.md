# How to Run the Application

This guide explains how to run the Natural Language Inventory Dashboard application on your local machine.

## Prerequisites

Before running the app, ensure you have:

- **Python 3.9+** installed ([Download Python](https://www.python.org/downloads/))
- **Node.js 18+** and npm installed ([Download Node.js](https://nodejs.org/))
- **Git** (if cloning from repository)

## Step-by-Step Instructions

### Step 1: Setup Backend (Python)

1. **Navigate to the backend directory:**
   ```powershell
   cd backend_python
   ```

2. **Create and activate virtual environment:**
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   ```
   
   If you get an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env` file in the `backend_python/` directory with the following content:
   
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
   
   # Azure OpenAI Configuration (if using Azure OpenAI)
   AZURE_OPENAI_API_KEY=your-azure-api-key-here
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   OPENAI_ENABLED=true
   
   # OR Standard OpenAI Configuration (if using standard OpenAI)
   # OPENAI_API_KEY=your-api-key-here
   # OPENAI_MODEL=gpt-4o-mini
   # OPENAI_ENABLED=true
   ```
   
   **Important:** Replace the API key and endpoint with your actual Azure OpenAI credentials.
   
   💡 **No API key?** The app will automatically fall back to keyword-based query generation, but GPT provides much better results.

5. **Start the backend server:**
   ```powershell
   python src\main.py
   ```
   
   You should see output like:
   ```
   INFO - Starting Natural Language Inventory Dashboard backend...
   INFO - Database connection successful
   INFO - Server listening on port 3001
   ```
   
   The backend will automatically create `inventory.db` with sample data on first run.

### Step 2: Setup Frontend (React)

1. **Open a NEW terminal window** (keep the backend running in the first terminal)

2. **Navigate to the frontend directory:**
   ```powershell
   cd frontend
   ```

3. **Install frontend dependencies (first time only):**
   ```powershell
   npm install
   ```

4. **Start the frontend development server:**
   ```powershell
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:3000/
   ➜  Network: use --host to expose
   ```

### Step 3: Access the Application

1. **Open your web browser** and navigate to:
   ```
   http://localhost:3000
   ```

2. **You should see the dashboard** with:
   - A query input field
   - Recent queries section
   - Results area (table and charts)

3. **Try a sample query**, such as:
   - "Show me top-selling products in electronics"
   - "List items with low stock"
   - "Show me products that need reordering"

## Quick Start (If Already Set Up)

If you've already completed the setup above, you can quickly start the app:

**Terminal 1 (Backend):**
```powershell
cd backend_python
.\venv\Scripts\Activate.ps1
python src\main.py
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev
```

Then open **http://localhost:3000** in your browser.

## Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError" or import errors**
- **Solution:** Make sure you activated the virtual environment (`.\venv\Scripts\Activate.ps1`)
- **Solution:** Reinstall dependencies: `pip install -r requirements.txt`

**Problem: "Database connection failed"**
- **Solution:** The database file will be created automatically on first run. Make sure you have write permissions in the `backend_python/` directory.

**Problem: "Port 3001 already in use"**
- **Solution:** Stop any process using port 3001, or change the `PORT` in `.env` file

**Problem: "OpenAI API error"**
- **Solution:** Check your `.env` file has the correct API key and endpoint
- **Solution:** The app will fall back to keyword-based queries if GPT is unavailable

### Frontend Issues

**Problem: "Cannot find module" errors**
- **Solution:** Run `npm install` in the `frontend/` directory

**Problem: "Network Error" when submitting queries**
- **Solution:** Make sure the backend is running on port 3001
- **Solution:** Check that `CORS_ORIGIN` in backend `.env` matches frontend URL (http://localhost:3000)

**Problem: "Port 3000 already in use"**
- **Solution:** Stop any process using port 3000, or the frontend will automatically use the next available port

### General Issues

**Problem: Both servers won't start**
- **Solution:** Make sure you're in the correct directories
- **Solution:** Check that all dependencies are installed
- **Solution:** Verify Python and Node.js versions meet requirements

**Problem: "Execution Policy" error in PowerShell**
- **Solution:** Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Stopping the Application

To stop the application:

1. **Stop the frontend:** Press `Ctrl+C` in the frontend terminal
2. **Stop the backend:** Press `Ctrl+C` in the backend terminal

## What's Running Where?

- **Backend API:** http://localhost:3001
  - Handles natural language queries
  - Converts queries to SQL
  - Executes database queries
  - Returns results as JSON

- **Frontend Dashboard:** http://localhost:3000
  - User interface for entering queries
  - Displays results in tables and charts
  - Shows query history

## Next Steps

Once the app is running:

1. Try different natural language queries
2. Explore the chart visualizations
3. Check the query history
4. Review the generated SQL queries (visible in browser console or backend logs)

For more information, see the main [README.md](README.md) file.

