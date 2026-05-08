#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8085}"

TMP_DIR="$(mktemp -d /tmp/iahx-modern-smoke.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT

curl_args=(-sS -L --connect-timeout 5 --max-time 30)
failures=0

run_request() {
  local name="$1"
  local path="$2"
  local body_file="$TMP_DIR/${name}.body"
  local response
  local status

  response="$(
    curl "${curl_args[@]}" \
      -w $'\n%{http_code}' \
      "${BASE_URL}${path}"
  )"
  status="${response##*$'\n'}"

  printf '%s\n' "${response%$'\n'*}" > "$body_file"
  printf '%s\n' "$status" > "$TMP_DIR/${name}.status"
}

assert_status() {
  local name="$1"
  local expected="$2"
  local status

  status="$(cat "$TMP_DIR/${name}.status")"
  if [[ "$status" != "$expected" ]]; then
    echo "not ok - ${name}: expected HTTP ${expected}, got ${status}"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: HTTP ${expected}"
}

assert_body_contains() {
  local name="$1"
  local expected="$2"

  if ! grep -iq "$expected" "$TMP_DIR/${name}.body"; then
    echo "not ok - ${name}: body does not contain '${expected}'"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: body contains '${expected}'"
}

assert_body_not_contains() {
  local name="$1"
  local unexpected="$2"

  if grep -iq "$unexpected" "$TMP_DIR/${name}.body"; then
    echo "not ok - ${name}: body contains '${unexpected}'"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: body does not contain '${unexpected}'"
}

echo "Smoke testing modern PHP at ${BASE_URL}"

run_request advanced "/advanced/?lang=en"
assert_status advanced 200
assert_body_contains advanced "Advanced Search"
assert_body_not_contains advanced "Fatal error"
assert_body_not_contains advanced "Warning:"

run_request bookmark_clear "/bookmark/c"
assert_status bookmark_clear 200
assert_body_contains bookmark_clear "0"
assert_body_not_contains bookmark_clear "Fatal error"
assert_body_not_contains bookmark_clear "Warning:"

run_request history "/history/?lang=en"
assert_status history 200
assert_body_contains history "Search History"
assert_body_not_contains history "Fatal error"
assert_body_not_contains history "Warning:"

if [[ "$failures" -gt 0 ]]; then
  echo "${failures} modern smoke assertion(s) failed"
  exit 1
fi

echo "All modern smoke tests passed"
