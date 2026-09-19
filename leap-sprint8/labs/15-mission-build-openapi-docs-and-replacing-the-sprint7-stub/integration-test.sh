#!/usr/bin/env bash
set -euo pipefail

# MISSION_SERVICE_DIR points at YOUR OWN Sprint 6/7 mission service
# checkout - the one whose SecurityConfig this script proves needs zero
# changes. Override it if your copy lives somewhere else:
#   MISSION_SERVICE_DIR=/path/to/it ./integration-test.sh
MISSION_SERVICE_DIR="${MISSION_SERVICE_DIR:-../../../leap-sprint6/solutions/13-mission-build-containerise-integration-test-wrap-up}"

NETWORK=mission-net
POSTGRES=sprint6-postgres
AUTH_IMAGE=sprint8-auth-service:m15
AUTH_CONTAINER=sprint8-auth-service-m15
SERVICE_IMAGE=mission-service:m15
SERVICE_CONTAINER=mission-service-m15
AUTH_PORT=3001
SERVICE_PORT=8081

cleanup() {
  echo "== Teardown =="
  docker rm -f "$AUTH_CONTAINER" "$SERVICE_CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "== Stage: Network =="
docker network create "$NETWORK" >/dev/null 2>&1 || true
docker network connect "$NETWORK" "$POSTGRES" >/dev/null 2>&1 || true

echo "== Stage: Build Images =="
docker build -t "$AUTH_IMAGE" .
docker build -t "$SERVICE_IMAGE" "$MISSION_SERVICE_DIR"

echo "== Stage: Run Containers =="
docker rm -f "$AUTH_CONTAINER" "$SERVICE_CONTAINER" >/dev/null 2>&1 || true
docker run -d --name "$AUTH_CONTAINER" --network "$NETWORK" -p "$AUTH_PORT:3000" "$AUTH_IMAGE"
docker run -d --name "$SERVICE_CONTAINER" --network "$NETWORK" -p "$SERVICE_PORT:8080" \
  -e SPRING_DATASOURCE_URL="jdbc:postgresql://$POSTGRES:5432/mission" \
  "$SERVICE_IMAGE"

# TODO 4: wait for both containers to be ready - poll the auth service's
# GET /health and the mission service's POST /accounts/1/orders (any
# non-000 curl code means it's answering), same retry-loop shape as
# Sprint 6, Module 13.

# TODO 5: smoke test - a request to POST /accounts/1/orders on the
# mission service with NO Authorization header must return 401. Exit 1
# with a clear message if it doesn't.

# TODO 6: end-to-end - log in against the NEW auth service
# (POST http://localhost:$AUTH_PORT/auth/login, alice/mission123), pull
# accessToken out of the response, then use it as a Bearer token to
# submit a real order to the mission service. Confirm the response
# contains "status":"ACCEPTED".

# TODO 7: confirm the order actually landed in Postgres - query the
# holdings/instruments join for account 1's ULVR.L quantity, the same
# way Sprint 6, Module 13 did.

echo "== ALL STAGES PASSED =="
