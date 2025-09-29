#!/bin/bash
set -e
cd "$(dirname "$0")/.."

BACKUP_DIR="backups"
TIMESTAMP=$(date +%F_%H-%M)

mkdir -p "$BACKUP_DIR"

tar -czvf "$BACKUP_DIR/full-backup-volumes-data-$TIMESTAMP.tar.gz" \
  volumes/jenkins \
  volumes/grafana \
  volumes/prometheus \
  data \
  config/docker-compose.yml \
  config/Jenkinsfile \
  config/prometheus.yml \
  requirements.txt

PARENT_BACKUP="$BACKUP_DIR/project-full-backup-$TIMESTAMP.tar.gz"
tar -czvf "$PARENT_BACKUP" \
  --exclude="$BACKUP_DIR" \
  .
