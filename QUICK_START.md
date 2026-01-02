# Quick Start Guide

## Deploy with Docker (Easiest)

### Prerequisites
- Docker Desktop installed and running
- Ports 80, 3001, and 5432 available

### Steps

1. **Windows (PowerShell):**
   ```powershell
   .\deploy.ps1
   ```

2. **Linux/Mac:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Or manually:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Open your browser to: http://localhost
   - The dashboard should be ready to use!

### Verify Deployment

Check service status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

## Deploy Without Docker

### Prerequisites
- Node.js 18+ and npm
- PostgreSQL database

### Steps

1. **Set up database:**
   - Create a PostgreSQL database named `inventory`
   - Run the SQL from `backend/init.sql` to create tables

2. **Configure backend:**
   ```bash
   cd backend
   npm install
   ```
   
   Create `backend/.env`:
   ```env
   PORT=3001
   NODE_ENV=development
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=inventory
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_SSL=false
   CORS_ORIGIN=http://localhost:3000
   LOG_LEVEL=info
   ```

3. **Start backend:**
   ```bash
   npm run dev
   ```

4. **Configure frontend:**
   ```bash
   cd frontend
   npm install
   ```

5. **Start frontend:**
   ```bash
   npm run dev
   ```

6. **Access the application:**
   - Open your browser to: http://localhost:3000

## Troubleshooting

### Docker Issues

**Docker not running:**
- Start Docker Desktop
- Wait for it to fully start
- Try deployment again

**Ports already in use:**
- Stop services using ports 80, 3001, or 5432
- Or change ports in `docker-compose.yml`

**Build fails:**
```bash
docker-compose build --no-cache
```

### Database Connection Issues

**Check database is running:**
```bash
docker-compose ps postgres
```

**View database logs:**
```bash
docker-compose logs postgres
```

**Reset database:**
```bash
docker-compose down -v
docker-compose up -d
```

### Application Not Loading

**Check backend health:**
```bash
curl http://localhost:3001/api/health
```

**Check frontend:**
- Open browser developer console
- Look for errors in Network tab
- Verify API URL in `frontend/src/config/index.ts`

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [README.md](README.md) for development setup
- Check service logs for detailed error messages

