#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PHP_IMAGE="${PHP_IMAGE:-php:8.5-cli}"

cd "$ROOT_DIR"

docker run --rm \
    -v "$ROOT_DIR:/app" \
    -w /app \
    "$PHP_IMAGE" \
    sh -lc '
        find iahx iahx-sites \
            -path iahx/lib/silex/vendor -prune -o \
            -name "*.php" -print |
        sort |
        while IFS= read -r file; do
            php -l "$file" >/tmp/php-lint.out 2>&1 || {
                cat /tmp/php-lint.out
                echo "failed: $file"
                exit 1
            }
        done
    '

echo "PHP compatibility lint passed with ${PHP_IMAGE}"
