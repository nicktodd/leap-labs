#!/usr/bin/env bash
# KATA: complete the network/build/run staging is given - your job is the
# verification stages below (Wait, Smoke Test, End-to-End, Confirm).
# Staged like the Jenkinsfiles from Sprint 1/2 - each stage should fail
# fast and loud, not silently.
set -euo pipefail

NETWORK=mission-net
POSTGRES=sprint6-postgres
AUTH_IMAGE=mission-auth-stub:m13lab
AUTH_CONTAINER=auth-stub-m13lab
SERVICE_IMAGE=mission-service:m13lab
SERVICE_CONTAINER=mission-service-m13lab
AUTH_PORT=4002
SERVICE_PORT=8084

cleanup() {
  echo "== Teardown =="
  docker rm -f "$AUTH_CONTAINER" "$SERVICE_CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "== Stage: Network =="
docker network create "$NETWORK" >/dev/null 2>&1 || true
docker network connect "$NETWORK" "$POSTGRES" >/dev/null 2>&1 || true

echo "== Stage: Build Images =="
docker build -t "$AUTH_IMAGE" ../../shared/auth-stub
docker build -t "$SERVICE_IMAGE" .

echo "== Stage: Run Containers =="
docker rm -f "$AUTH_CONTAINER" "$SERVICE_CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$AUTH_CONTAINER" --network "$NETWORK" -p "$AUTH_PORT:4000" "$AUTH_IMAGE"
docker run -d --name "$SERVICE_CONTAINER" --network "$NETWORK" -p "$SERVICE_PORT:8080" \
  -e SPRING_DATASOURCE_URL="jdbc:postgresql://$POSTGRES:5432/mission" \
  "$SERVICE_IMAGE"

echo "== Stage: Wait for Both to Be Ready =="
echo "  Waiting for auth stub on port $AUTH_PORT ..."
for i in $(seq 1 30); do
  if curl -sf "http://localhost:$AUTH_PORT/health" >/dev/null 2>&1; then
    echo "  Auth stub is ready."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "FAIL: auth stub did not become ready in time"
    exit 1
  fi
  sleep 2
done

echo "  Waiting for mission service on port $SERVICE_PORT ..."
for i in $(seq 1 45); do
  if curl -sf -o /dev/null -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
      -H "Content-Type: application/json" -d '{}' 2>/dev/null; then
    echo "  Mission service is ready."
    break
  fi
  # Accept any HTTP response (including 401/400) - that means the service is up
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
      -H "Content-Type: application/json" -d '{}' 2>/dev/null || true)
  if [ -n "$STATUS" ] && [ "$STATUS" != "000" ]; then
    echo "  Mission service is ready (HTTP $STATUS)."
    break
  fi
  if [ "$i" -eq 45 ]; then
    echo "FAIL: mission service did not become ready in time"
    exit 1
  fi
  sleep 2
done

echo "== Stage: Smoke Test - No Token Is Rejected =="
SMOKE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "http://localhost:$SERVICE_PORT/accounts/1/orders" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":5,"price":40.0,"side":"BUY"}')
if [ "$SMOKE_STATUS" != "401" ]; then
  echo "FAIL: expected 401 for unauthenticated request, got $SMOKE_STATUS"
  exit 1
fi
echo "PASS: unauthenticated request returned 401"

echo "== Stage: End-to-End Authenticated Order =="
TOKEN=$(curl -s -X POST "http://localhost:$AUTH_PORT/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}' \
  | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')

if [ -z "$TOKEN" ]; then
  echo "FAIL: could not obtain a token from the containerised auth stub"
  exit 1
fi
echo "  Token obtained from containerised auth stub."

ORDER_RESPONSE=$(curl -s -X POST "http://localhost:$SERVICE_PORT/accounts/1/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"ticker":"ULVR.L","instrumentType":"EQUITY","quantity":5,"price":40.0,"side":"BUY"}')

if echo "$ORDER_RESPONSE" | grep -q '"ACCEPTED"'; then
  echo "PASS: authenticated order returned ACCEPTED"
else
  echo "FAIL: expected ACCEPTED in response, got: $ORDER_RESPONSE"
  exit 1
fi

echo "== Stage: Confirm It Actually Landed in Postgres =="
DB_RESULT=$(docker exec -e PGPASSWORD=mission "$POSTGRES" psql -U postgres -d mission -t -c \
  "SELECT h.quantity FROM holdings h JOIN instruments i ON h.instrument_id=i.instrument_id WHERE h.account_id=1 AND i.ticker='ULVR.L';")

if [ -z "$(echo "$DB_RESULT" | tr -d '[:space:]')" ]; then
  echo "FAIL: no holding row found in Postgres for account 1 / ULVR.L"
  exit 1
fi
echo "PASS: holding confirmed in Postgres: quantity =$(echo "$DB_RESULT" | tr -d '[:space:]')"

echo "== ALL STAGES PASSED =="
