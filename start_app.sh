#!/bin/bash

echo "=== Starting pyme-app Flask Application ==="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if database is running
echo "Checking database connection..."
if ! docker-compose ps | grep -q "aroma-app-db.*Up"; then
    echo "❌ Database is not running. Please start the database first:"
    echo "   ./start_db.sh"
    exit 1
fi

# Initialize database (if needed)
echo "Initializing database..."
python init_db.py

# Start the Flask application
echo "Starting Flask application..."
echo "🌐 Application will be available at: http://localhost:8000"
echo "🔍 Debug info available at: http://localhost:8000/debug"
echo "💾 Database test available at: http://localhost:8000/db-test"
echo ""
echo "Press Ctrl+C to stop the server"

# Set environment variables
export FLASK_ENV=development
export DATABASE_URL=postgresql://pyme_user:pyme_password@localhost:5432/aroma_app_db

# Start the application
python app.py 