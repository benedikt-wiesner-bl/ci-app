#!/bin/bash
set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%F_%H-%M)

mkdir -p $BACKUP_DIR

tar -czvf $BACKUP_DIR/full-backup-volumes-data-$TIMESTAMP.tar.gz \
  volumes/jenkins \
  volumes/grafana \
  volumes/prometheus \
  data \
  docker-compose.yml \
  Jenkinsfile \
  prometheus.yml \
  requirements.txt

PARENT_BACKUP="../project-full-backup-$TIMESTAMP.tar.gz"
tar -czvf "$PARENT_BACKUP"