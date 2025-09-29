#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

DOCKER_COMPOSE_FILE="config/docker-compose.yml"

GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
RESET="\e[0m"

usage() {
  echo -e "Usage: $0 [-start] [-stop] [-build] [-h|--help]\n"
  echo "  -start   Starts Docker and starts docker compose"
  echo "  -stop    Stops docker compose"
  echo "  -build   Starts Docker and build docker compose new (DO ON FIRST USAGE)"
  exit 1
}

start_docker() {
  echo -e "${YELLOW}Starting Docker in WSL...${RESET}"
  sudo service docker start
}

compose_up() {
  echo -e "${GREEN}Starting docker compose...${RESET}"
  docker compose -f "$DOCKER_COMPOSE_FILE" up -d
}

compose_build() {
  echo -e "${GREEN}Building new docker compose...${RESET}"
  docker compose -f "$DOCKER_COMPOSE_FILE" up -d --build
}

compose_down() {
  echo -e "${RED}Stopping docker compose...${RESET}"
  docker compose -f "$DOCKER_COMPOSE_FILE" down
}

if [ $# -eq 0 ]; then
  usage
fi

for arg in "$@"; do
  case $arg in
    -start) start_docker; compose_up ;;
    -stop)  compose_down ;;
    -build) start_docker; compose_build ;;
    -h|--help) usage ;;
    *) echo -e "${RED}Error: $arg${RESET}"; usage ;;
  esac
done
