#!/bin/bash
echo "Starte Docker in WSL..."
sudo service docker start
echo "Starte docker compose..."
docker compose up -d
