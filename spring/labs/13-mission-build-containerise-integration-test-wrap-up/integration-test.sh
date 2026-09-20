#!/usr/bin/env bash
# KATA: complete the network/build/run staging is given - your job is the
# verification stages below (Wait, Smoke Test, End-to-End, Confirm).
# Staged like the Jenkinsfiles from Sprint 1/2 - each stage should fail
# fast and loud, not silently.
set -euo pipefail

NETWORK=mission-net
POSTGRES=missionservice-postgres
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
# TODO 1: poll http://localhost:$AUTH_PORT/health in a retry loop until it
# responds (up to ~30 tries, 2s apart). Remember set -e's gotcha: a plain
# `curl ... && break` inside a loop will kill the whole script the FIRST
# time curl fails while the container is still starting - wrap it in
# `if ...; then break; fi` instead.

# TODO 2: same idea, but poll SERVICE_PORT with a POST to
# /accounts/1/orders (any body is fine - you're only checking it responds
# at all, not that the response is meaningful yet).
echo "TODO 1/2 not implemented"; exit 1

echo "== Stage: Smoke Test - No Token Is Rejected =="
# TODO 3: POST a well-formed order to $SERVICE_PORT with NO Authorization
# header. Capture the HTTP status code (curl -o /dev/null -w "%{http_code}").
# Fail the script (echo a clear message, exit 1) if it isn't 401.
echo "TODO 3 not implemented"; exit 1

echo "== Stage: End-to-End Authenticated Order =="
# TODO 4: POST to $AUTH_PORT/login (alice / mission123) to get a real
# token from the CONTAINERISED auth stub. Extract the token from the JSON
# response - `sed -n 's/.*"token":"\([^"]*\)".*/\1/p'` works without
# needing any extra tooling.

# TODO 5: use that token to POST a real order to $SERVICE_PORT. Fail loudly
# if the response doesn't contain "ACCEPTED".
echo "TODO 4/5 not implemented"; exit 1

echo "== Stage: Confirm It Actually Landed in Postgres =="
# TODO 6: query the holdings/instruments join for account 1's ULVR.L
# holding directly against $POSTGRES via `docker exec ... psql ...` - the
# same query the demo used. This is your proof the write really happened,
# not just that the HTTP response claimed it did.
echo "TODO 6 not implemented"; exit 1

echo "== ALL STAGES PASSED =="
