#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/.env"

echo "Initializing host storage environment at ${HOMEBOX_DATA_DIR}..."

mkdir -p "$HOMEBOX_DATA_DIR"

# Force permissions to match Homebox rootless UID
chown -R 65532:65532 "$HOMEBOX_DATA_DIR"
chmod 750 "$HOMEBOX_DATA_DIR"

echo "Permissions applied successfully."
