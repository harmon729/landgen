#!/bin/bash

echo "🚀 LandGen Development Server"
echo "================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "⚠️  Warning: .env.local not found"
    echo "Creating from template..."
    cp .env.local.example .env.local
    echo "✅ Created .env.local - Please add your GEMINI_API_KEY"
    echo ""
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    echo ""
fi

if [ ! -f "api/__pycache__" ]; then
    echo "📦 Installing backend dependencies..."
    cd api
    pip3 install -r requirements.txt
    cd ..
    echo ""
fi

# Start the dev servers
echo "🔥 Starting development servers..."
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev:all

