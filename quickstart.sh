#!/bin/bash

# Financial AI Agent Platform - Quick Start Script
# This script helps you get started quickly with the platform

set -e

echo "🚀 Financial AI Agent Platform - Quick Start"
echo "============================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys:"
    echo "   - GEMINI_API_KEY"
    echo "   - MARKET_DATA_API_KEY"
    echo "   - MARKET_DATA_SECRET_KEY (if using Alpaca)"
    echo "   - NEWS_API_KEY"
    echo "   - SECRET_KEY (generate a secure random string)"
    echo ""
    echo "After editing .env, run this script again."
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose is installed"
echo ""

# Validate .env file has required keys
required_keys=("GEMINI_API_KEY" "MARKET_DATA_API_KEY" "NEWS_API_KEY" "SECRET_KEY")
missing_keys=()

for key in "${required_keys[@]}"; do
    if ! grep -q "^$key=.\+" .env; then
        missing_keys+=("$key")
    fi
done

if [ ${#missing_keys[@]} -gt 0 ]; then
    echo "❌ Missing required API keys in .env file:"
    for key in "${missing_keys[@]}"; do
        echo "   - $key"
    done
    echo ""
    echo "Please edit .env file and add the missing keys."
    exit 1
fi

echo "✅ All required API keys are configured"
echo ""

# Start services
echo "🐳 Starting services with Docker Compose..."
echo ""

docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Access the application:"
    echo "   Frontend:  http://localhost:8501"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📋 View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose down"
    echo ""
    echo "🎉 Setup complete! Visit http://localhost:8501 to get started."
    echo ""
else
    echo ""
    echo "❌ Some services failed to start. Check logs with:"
    echo "   docker-compose logs"
    exit 1
fi
