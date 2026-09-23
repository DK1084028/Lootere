#!/usr/bin/env bash
set -e
echo "🚀 Deploying PROJECT LOOTERE..."
docker compose build --parallel
docker compose up -d
echo "✅ DEPLOYMENT COMPLETE!"
