#!/bin/bash

# Run Instagram bot with Docker Compose

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create .env file with your Instagram credentials:"
    echo "cp .env.example .env"
    echo "Then edit .env and add your username and password"
    exit 1
fi

# Check if credentials are set
source .env
if [ -z "$INSTAGRAM_USERNAME" ] || [ -z "$INSTAGRAM_PASSWORD" ]; then
    echo "❌ Error: Instagram credentials not set in .env file!"
    exit 1
fi

echo "🚀 Starting Instagram bot..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Bot started successfully!"
    echo ""
    echo "Commands:"
    echo "- View logs: docker-compose logs -f"
    echo "- Stop bot: docker-compose down"
    echo "- Restart bot: docker-compose restart"
else
    echo "❌ Failed to start bot"
    exit 1
fi