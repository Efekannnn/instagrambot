#!/bin/bash

# Stop Instagram bot

echo "🛑 Stopping Instagram bot..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "✅ Bot stopped successfully!"
else
    echo "❌ Failed to stop bot"
    exit 1
fi