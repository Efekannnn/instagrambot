#!/bin/bash

# Run multiple Instagram bots with Docker Compose

# Check if .env.multi file exists
if [ ! -f ".env.multi" ]; then
    echo "❌ Error: .env.multi file not found!"
    echo ""
    echo "Please create .env.multi file with your bot credentials:"
    echo "cp .env.multi.example .env.multi"
    echo "Then edit .env.multi and add credentials for each bot"
    exit 1
fi

echo "🚀 Starting multiple Instagram bots..."
docker-compose -f docker-compose.multi.yml --env-file .env.multi up -d

if [ $? -eq 0 ]; then
    echo "✅ All bots started successfully!"
    echo ""
    echo "Commands:"
    echo "- View all logs: docker-compose -f docker-compose.multi.yml logs -f"
    echo "- View specific bot: docker-compose -f docker-compose.multi.yml logs -f instagram-bot-1"
    echo "- Stop all bots: ./scripts/stop-multi.sh"
    echo "- Check status: docker-compose -f docker-compose.multi.yml ps"
else
    echo "❌ Failed to start bots"
    exit 1
fi