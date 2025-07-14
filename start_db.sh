#!/bin/bash

echo "=== Starting PostgreSQL Database (aroma-app-db) ==="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop existing containers if running
echo "Stopping existing containers..."
docker-compose down

# Start the database
echo "Starting PostgreSQL database..."
docker-compose up -d aroma-app-db

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Check database health
echo "Checking database health..."
if docker-compose exec -T aroma-app-db pg_isready -U pyme_user -d aroma_app_db; then
    echo "✅ PostgreSQL database is ready!"
    echo "📊 Database URL: postgresql://pyme_user:pyme_password@localhost:5432/aroma_app_db"
    echo "🔧 pgAdmin available at: http://localhost:5050"
    echo "   Email: admin@example.com"
    echo "   Password: admin123"
else
    echo "❌ Database is not ready yet. Please wait a moment and try again."
    exit 1
fi

echo ""
echo "=== Database Setup Complete ==="
echo "Next steps:"
echo "1. Run: python init_db.py (to initialize tables and data)"
echo "2. Run: python app.py (to start the Flask application)"
echo "3. Visit: http://localhost:8000 (to access the application)" 