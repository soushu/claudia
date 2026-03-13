#!/bin/bash
set -euo pipefail

DEPLOY_DIR="/home/yutookiguchi/claudia-staging"
BRANCH="develop"
SUDO_USER="sudo -u yutookiguchi"

echo "=== Deploying STAGING (${BRANCH}) ==="

cd "$DEPLOY_DIR"

# Pull latest code
$SUDO_USER git fetch origin "$BRANCH"
$SUDO_USER git reset --hard "origin/${BRANCH}"

# Backend: install dependencies + migrate
$SUDO_USER venv/bin/pip install -q -r requirements.txt
$SUDO_USER venv/bin/alembic upgrade head

# Frontend: install dependencies + build
cd frontend
$SUDO_USER npm ci --prefer-offline
$SUDO_USER bash -c 'NODE_OPTIONS="--max_old_space_size=512" npm run build'
cd ..

# Restart services
sudo systemctl restart claudia-staging-backend
sudo systemctl restart claudia-staging-frontend

# Wait for backend to be ready
echo "Waiting for backend..."
for i in $(seq 1 30); do
  if curl -sf http://127.0.0.1:8001/health > /dev/null 2>&1; then
    echo "Backend is healthy"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "ERROR: Backend failed to start"
    sudo journalctl -u claudia-staging-backend --no-pager -n 20
    exit 1
  fi
  sleep 1
done

echo "=== Staging deploy complete ==="
