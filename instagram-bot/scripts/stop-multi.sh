#!/bin/bash

# Stop all Instagram bots

echo "🛑 Stopping all Instagram bots..."
docker-compose -f docker-compose.multi.yml down

if [ $? -eq 0 ]; then
    echo "✅ All bots stopped successfully!"
else
    echo "❌ Failed to stop bots"
    exit 1
fi