#!/usr/bin/env bash
set -euo pipefail

if [ ! -f vendor-modern/autoload.php ]; then
    docker compose -f docker-compose-php85.yml build php85
    docker compose -f docker-compose-php85.yml run --rm php85 composer install --no-interaction --no-progress --working-dir=/app
fi

docker compose -f docker-compose-php85.yml run --rm php85 php -d display_errors=1 tests/php_compat/modern_scielo_index.php
