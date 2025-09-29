#!/bin/bash

# Build Docker image for Instagram bot

echo "Building Instagram bot Docker image..."

# Build the Docker image
docker build -t instagram-bot .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the bot:"
    echo "1. Copy .env.example to .env and add your credentials"
    echo "2. Run: ./scripts/run.sh"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi