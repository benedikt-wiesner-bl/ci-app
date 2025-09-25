#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Starte Docker in WSL..."
sudo service docker start
echo "Starte docker compose..."
docker compose -f config/docker-compose.yml up -d
