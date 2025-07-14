#!/bin/bash

echo "=== Starting pyme-app for Render Free Tier ==="

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

# Set environment variables for free tier
export FLASK_ENV=production
export RENDER=true
export DATABASE_URL=sqlite:///pyme_app.db

# Initialize database with SQLite
echo "Initializing SQLite database..."
python init_db.py

# Start the Flask application
echo "Starting Flask application..."
echo "🌐 Application will be available at: http://localhost:8000"
echo "🔍 Debug info available at: http://localhost:8000/debug"
echo "💾 Database test available at: http://localhost:8000/db-test"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the application
python app.py 