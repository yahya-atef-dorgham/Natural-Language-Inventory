#!/bin/bash

# Deployment script for Natural Language Inventory Dashboard

set -e

echo "🚀 Starting deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << EOF
DB_NAME=inventory
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
EOF
    echo "✅ .env file created. Please update it with your database credentials."
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
if docker-compose ps | grep -q "healthy"; then
    echo "✅ Services are healthy!"
else
    echo "⚠️  Some services may not be healthy. Check logs with: docker-compose logs"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Services:"
echo "  - Frontend: http://localhost"
echo "  - Backend API: http://localhost:3001"
echo "  - Database: localhost:5432"
echo ""
echo "📝 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - View status: docker-compose ps"
echo ""

