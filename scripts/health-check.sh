#!/bin/bash
# health-check.sh
# Demonstrates a basic automated health check for the cloud-service-baseline.

TARGET_URL=${1:-"http://localhost:8000/health"}
MAX_RETRIES=5
RETRY_INTERVAL=5

echo "Starting health check for $TARGET_URL..."

for ((i=1; i<=MAX_RETRIES; i++)); do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL")
    
    if [ "$STATUS_CODE" -eq 200 ]; then
        echo "SUCCESS: Service is healthy (HTTP 200)"
        exit 0
    else
        echo "RETRY $i/$MAX_RETRIES: Service returned HTTP $STATUS_CODE. Waiting $RETRY_INTERVAL seconds..."
        sleep "$RETRY_INTERVAL"
    fi
done

echo "FAILURE: Service failed health check after $MAX_RETRIES attempts."
exit 1
