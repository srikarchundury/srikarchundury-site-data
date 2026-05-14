#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

REMOTE_NAME="origin"
BRANCH_NAME="main"
COMMIT_MESSAGE="${1:-}"
PASSWORD="${SCRAMBLE_PASSWORD:-}"

if [[ -z "$PASSWORD" ]]; then
  read -r -s -p "Scramble password: " PASSWORD
  echo
fi

if [[ -z "$PASSWORD" ]]; then
  echo "Error: scramble password is required."
  exit 1
fi

if [[ -z "$COMMIT_MESSAGE" ]]; then
  COMMIT_MESSAGE="Update site data $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo "[publish_site_data] Working directory: $ROOT_DIR"
echo "[publish_site_data] Scrambling data files..."
./scramble.sh --password "$PASSWORD"

echo "[publish_site_data] Staging changes..."
git add -A

if git diff --cached --quiet; then
  echo "[publish_site_data] No changes to commit."
  exit 0
fi

echo "[publish_site_data] Creating commit..."
git commit -m "$COMMIT_MESSAGE"

echo "[publish_site_data] Pushing to $REMOTE_NAME/$BRANCH_NAME..."
git push "$REMOTE_NAME" "$BRANCH_NAME"

echo "[publish_site_data] Done."
