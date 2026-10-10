#!/usr/bin/env bash
# Scan de securite local, equivalent des stages du pipeline CI (arret au premier echec).
# Usage : bash scripts/local-scan.sh      (necessite Docker)
set -e
cd "$(dirname "$0")/.."

echo "=== 1/4 Secrets (Gitleaks) ==="
docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest detect --source /repo \
  --config /repo/.gitleaks.toml --baseline-path /repo/gitleaks-baseline.json

echo "=== 2/4 SAST (Bandit, severite MEDIUM ou plus) ==="
docker run --rm -v "$PWD:/src" python:3.12-slim sh -c \
  "pip install -q bandit && bandit -q -r /src/app --severity-level medium"

echo "=== 3/4 SCA (Trivy, CRITICAL/HIGH corrigeables) ==="
docker run --rm -v "$PWD:/src" aquasec/trivy:latest fs --severity CRITICAL,HIGH \
  --ignore-unfixed --exit-code 1 --quiet /src/app

echo "=== 4/4 IaC (Checkov : Terraform et Dockerfile) ==="
docker run --rm -v "$PWD:/src" bridgecrew/checkov:latest -d /src/infra --compact --quiet
docker run --rm -v "$PWD:/src" bridgecrew/checkov:latest -f /src/Dockerfile --compact --quiet

echo "OK : tous les controles locaux sont passes."
