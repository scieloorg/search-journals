#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1}"
HOST_HEADER="${HOST_HEADER:-}"
JSON_ACCESS_TOKEN="${JSON_ACCESS_TOKEN:-}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

curl_args=(-sS -L --connect-timeout 5 --max-time 30)
if [[ -n "$HOST_HEADER" ]]; then
  curl_args+=(-H "Host: $HOST_HEADER")
fi

failures=0

run_request() {
  local name="$1"
  local path="$2"
  local body_file="$TMP_DIR/${name}.body"
  local headers_file="$TMP_DIR/${name}.headers"
  local status

  status="$(
    curl "${curl_args[@]}" \
      -D "$headers_file" \
      -o "$body_file" \
      -w '%{http_code}' \
      "${BASE_URL}${path}"
  )"

  printf '%s\n' "$status" > "$TMP_DIR/${name}.status"
  printf '%s\n' "$body_file"
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

assert_header_contains() {
  local name="$1"
  local expected="$2"

  if ! grep -iq "$expected" "$TMP_DIR/${name}.headers"; then
    echo "not ok - ${name}: missing header matching '${expected}'"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: header contains '${expected}'"
}

assert_body_contains() {
  local name="$1"
  local expected="$2"
  local body_file="$TMP_DIR/${name}.body"

  if ! grep -iq "$expected" "$body_file"; then
    echo "not ok - ${name}: body does not contain '${expected}'"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: body contains '${expected}'"
}

assert_body_not_contains() {
  local name="$1"
  local unexpected="$2"
  local body_file="$TMP_DIR/${name}.body"

  if grep -iq "$unexpected" "$body_file"; then
    echo "not ok - ${name}: body contains '${unexpected}'"
    failures=$((failures + 1))
    return
  fi

  echo "ok - ${name}: body does not contain '${unexpected}'"
}

echo "Smoke testing ${BASE_URL}"
if [[ -n "$HOST_HEADER" ]]; then
  echo "Using Host header: ${HOST_HEADER}"
fi

run_request home "/?lang=pt&count=1" >/dev/null
assert_status home 200
assert_header_contains home "content-type: text/html"
assert_body_contains home "SciELO"
assert_body_not_contains home "Fatal error"
assert_body_not_contains home "Warning:"

run_request search "/?q=malaria&lang=en&count=1" >/dev/null
assert_status search 200
assert_header_contains search "content-type: text/html"
assert_body_contains search "SciELO"
assert_body_not_contains search "Fatal error"
assert_body_not_contains search "Warning:"

json_path="/?q=malaria&lang=en&count=1&output=json"
if [[ -n "$JSON_ACCESS_TOKEN" ]]; then
  json_path="${json_path}&access_token=${JSON_ACCESS_TOKEN}"
fi

run_request json "$json_path" >/dev/null
assert_status json 200
assert_header_contains json "content-type: application/json"
assert_body_contains json "diaServerResponse"
assert_body_not_contains json "Fatal error"
assert_body_not_contains json "Warning:"

run_request rss "/?q=malaria&lang=en&count=1&output=rss" >/dev/null
assert_status rss 200
assert_header_contains rss "content-type: text/xml"
assert_body_contains rss "<rss"
assert_body_not_contains rss "Fatal error"
assert_body_not_contains rss "Warning:"

run_request csv "/?q=malaria&lang=en&count=1&output=csv" >/dev/null
assert_status csv 200
assert_header_contains csv "content-type: text/csv"
assert_body_not_contains csv "Fatal error"
assert_body_not_contains csv "Warning:"

if [[ "$failures" -gt 0 ]]; then
  echo "${failures} smoke assertion(s) failed"
  exit 1
fi

echo "All smoke tests passed"
