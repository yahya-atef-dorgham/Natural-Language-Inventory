# Deployment Guide: Natural Language Inventory Dashboard

This guide covers deploying the Natural Language Inventory Dashboard using Docker and Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- At least 2GB of available RAM
- Ports 80, 3001, and 5432 available

## Quick Start

### Option 1: Using Docker Compose (Recommended)

**Windows (PowerShell):**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Manual deployment:**
```bash
docker-compose up -d
```

### Option 2: Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t nl-inventory-backend .
docker run -p 3001:3001 --env-file .env nl-inventory-backend
```

**Frontend:**
```bash
cd frontend
docker build -t nl-inventory-frontend .
docker run -p 80:80 nl-inventory-frontend
```

## Configuration

### Environment Variables

The application uses SQLite with automatic schema initialization. No additional configuration is required.

Optionally, create a `.env` file in the project root to customize settings:

```env
PORT=3001
NODE_ENV=production
DB_PATH=/app/data/inventory.db
LOG_LEVEL=info
```

The deployment script will create a default `.env` file if it doesn't exist.

### Database Setup

The Docker Compose setup includes:
- SQLite database with automatic initialization
- Sample data for testing
- Persistent storage via Docker volumes

The database schema and sample data are automatically created on first startup.

## Service URLs

After deployment, the services will be available at:

- **Frontend Dashboard**: http://localhost
- **Backend API**: http://localhost:3001
- **API Health Check**: http://localhost:3001/api/health

## Managing the Deployment

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### View Status

```bash
docker-compose ps
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

## Production Deployment

### Security Considerations

1. **Use HTTPS**: Configure reverse proxy (nginx/traefik) with SSL certificates
2. **Database security**: Secure the SQLite database file with proper file permissions
3. **Environment variables**: Use secrets management (Docker secrets, Kubernetes secrets, etc.)
4. **Network security**: Use firewall rules to restrict access to services
5. **Backup strategy**: Regularly backup the SQLite database file

### Production Docker Compose Override

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    environment:
      NODE_ENV: production
      LOG_LEVEL: warn
    restart: always

  frontend:
    restart: always

  postgres:
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Deploy with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Cloud Deployment Options

#### AWS (ECS/EKS)
- Use AWS ECR for container registry
- Deploy with ECS Fargate or EKS
- Use EFS or S3 for SQLite database persistence

#### Azure (Container Instances/AKS)
- Use Azure Container Registry
- Deploy with Azure Container Instances or AKS
- Use Azure Files for SQLite database persistence

#### Google Cloud (Cloud Run/GKE)
- Use Google Container Registry
- Deploy with Cloud Run or GKE
- Use Cloud Storage or Persistent Disks for SQLite database persistence

#### Heroku
- Use Heroku Container Registry
- Deploy with `heroku container:push`
- Note: Heroku's ephemeral filesystem requires external storage for database persistence

## Troubleshooting

### Services won't start

1. Check Docker is running: `docker info`
2. Check port availability: `netstat -an | grep -E '80|3001|5432'`
3. View logs: `docker-compose logs`

### Database connection errors

1. Check if database file exists: `docker-compose exec backend ls -la /app/data/`
2. Check environment variables: `docker-compose config`
3. Test connection: `docker-compose exec backend node -e "require('./dist/services/db').testConnection()"`
4. Check file permissions: Ensure the backend container can write to `/app/data/`

### Frontend can't reach backend

1. Check CORS configuration in `backend/src/config/index.ts`
2. Verify API URL in `frontend/src/config/index.ts`
3. Check nginx proxy configuration in `frontend/nginx.conf`

### Build failures

1. Clear Docker cache: `docker-compose build --no-cache`
2. Remove old images: `docker system prune -a`
3. Check Dockerfile syntax

## Health Checks

All services include health checks:

- **Backend**: `GET /api/health`
- **Frontend**: HTTP 200 on root path
- **Database**: `pg_isready` command

Check health status:
```bash
docker-compose ps
```

## Backup and Restore

### Backup Database

```bash
# Backup SQLite database
docker-compose exec backend cat /app/data/inventory.db > backup.db

# Or copy from volume
docker cp nl-inventory-backend:/app/data/inventory.db ./backup.db
```

### Restore Database

```bash
# Restore SQLite database
docker cp ./backup.db nl-inventory-backend:/app/data/inventory.db

# Restart backend to reload
docker-compose restart backend
```

## Monitoring

### Resource Usage

```bash
docker stats
```

### Service Health

```bash
curl http://localhost:3001/api/health
```

## Scaling

To scale backend services:

```bash
docker-compose up -d --scale backend=3
```

Note: You'll need a load balancer (nginx, traefik) in front of multiple backend instances.

## Rollback

To rollback to a previous version:

```bash
# Stop current services
docker-compose down

# Tag and pull previous image
docker pull your-registry/nl-inventory-backend:previous-version

# Update docker-compose.yml to use previous image
# Then restart
docker-compose up -d
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review this documentation
3. Check GitHub issues (if applicable)

