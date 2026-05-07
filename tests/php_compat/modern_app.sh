#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

docker compose -f docker-compose-php85.yml run --rm --build php85 composer install --no-interaction --no-scripts --no-plugins
docker compose -f docker-compose-php85.yml run --rm php85 php tests/php_compat/modern_app.php
