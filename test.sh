#!/bin/bash
set -e
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
  echo "Usage: $0 [-start] [-stop] [-build]"
  exit 1
fi

for arg in "$@"; do
  case $arg in
    -start) echo "Starting Docker in WSL..."
            sudo service docker start
            echo "Starting docker compose..."
            docker compose -f config/docker-compose.yml up -d;;
    -stop)  echo "Stopping Docker in WSL..."
            sudo service docker start
            echo "Stopping docker compose..."
            docker compose -f config/docker-compose.yml down;;
    -build) echo "Starting Docker in WSL..."
            sudo service docker start
            echo "Building docker compose..."
            docker compose -f config/docker-compose.yml up -d --build;;
    *) echo "Unknown option: $arg" ;;
  esac
done
