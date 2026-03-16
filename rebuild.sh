#!/bin/bash
set -euo pipefail

IMAGE_NAME="cr-backoffice"
CONTAINER_NAME="cr-backoffice-app"
HOST_PORT="${HOST_PORT:-8081}"

echo "Stopping existing containers..."
docker stop "$(docker ps -q --filter "name=${CONTAINER_NAME}")" 2>/dev/null || true
docker rm "$(docker ps -aq --filter "name=${CONTAINER_NAME}")" 2>/dev/null || true

echo "Rebuilding image..."
docker build -t "${IMAGE_NAME}" .

echo "Starting new container..."
docker run -d \
  -p "${HOST_PORT}":8080 \
  --env-file .env \
  --name "${CONTAINER_NAME}" \
  "${IMAGE_NAME}"

sleep 2
if [ "$(docker inspect -f '{{.State.Running}}' "${CONTAINER_NAME}" 2>/dev/null || echo "false")" != "true" ]; then
  echo "Container failed to start. Logs:"
  docker logs "${CONTAINER_NAME}" || true
  exit 1
fi

echo "Container started! Access at http://localhost:${HOST_PORT}/docs"
