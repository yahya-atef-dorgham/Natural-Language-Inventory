# Deployment script for Natural Language Inventory Dashboard (PowerShell)

Write-Host "🚀 Starting deployment..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if docker-compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ docker-compose is not installed. Please install docker-compose and try again." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    @"
DB_NAME=inventory
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ .env file created. Please update it with your database credentials." -ForegroundColor Green
}

# Build and start services
Write-Host "🔨 Building Docker images..." -ForegroundColor Yellow
docker-compose build

Write-Host "🚀 Starting services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host "🏥 Checking service health..." -ForegroundColor Yellow
$psOutput = docker-compose ps
if ($psOutput -match "healthy") {
    Write-Host "✅ Services are healthy!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some services may not be healthy. Check logs with: docker-compose logs" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Services:" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost" -ForegroundColor White
Write-Host "  - Backend API: http://localhost:3001" -ForegroundColor White
Write-Host "  - Database: localhost:5432" -ForegroundColor White
Write-Host ""
Write-Host "📝 Useful commands:" -ForegroundColor Cyan
Write-Host "  - View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "  - Stop services: docker-compose down" -ForegroundColor White
Write-Host "  - Restart services: docker-compose restart" -ForegroundColor White
Write-Host "  - View status: docker-compose ps" -ForegroundColor White
Write-Host ""

