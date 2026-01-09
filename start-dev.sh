#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Dev Environment..."

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Start Backend
echo "📦 Setting up Backend (Django)..."
cd backend

# Use existing venv
if [ -d "venv" ]; then
    echo "✅ Using existing virtual environment"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

source venv/bin/activate

# Load .env file
if [ -f ".env" ]; then
    echo "✅ Loading environment variables from .env"
    set -a
    source .env
    set +a
fi

python manage.py migrate --run-syncdb
echo "🟢 Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Start Frontend
echo "📦 Setting up Frontend (Vite)..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing..."
    npm install
fi

echo "🟢 Starting Vite dev server on port 5173..."
npm run dev -- --host &
FRONTEND_PID=$!

echo ""
echo "======================================="
echo "✅ Development servers are running!"
echo "---------------------------------------"
echo "🔗 Backend:  http://localhost:8000"
echo "🔗 Frontend: http://localhost:5173"
echo "======================================="
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for processes
wait
