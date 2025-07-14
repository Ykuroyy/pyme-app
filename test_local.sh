#!/bin/bash

echo "=== pyme-app ローカルテスト ==="

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

# Set environment variables for local testing
export FLASK_ENV=development
export DATABASE_URL=sqlite:///pyme_app.db

# Initialize database
echo "Initializing database..."
python init_db.py

# Run tests
echo "Running tests..."
python -m pytest test_app.py -v

# Start the application
echo "Starting Flask application for testing..."
echo "🌐 Application will be available at: http://localhost:8000"
echo "🔍 Debug info available at: http://localhost:8000/debug"
echo "💾 Database test available at: http://localhost:8000/db-test"
echo "🏥 Health check available at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the application
python app.py 