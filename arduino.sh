#!/bin/bash
# run.sh

# Get the session identifier from the first argument, defaulting to "unknown" if missing
SESSION_ID=${1:-"unknown"}

# Define environment variables
WEBHOOK_URL="https://webhook.site/b515c902-f0a9-497e-834e-ee60d14b2450"
WORK_DIR="/home/pi/chessbot/Chessbot_rasbpy"

# Execute run2.sh and capture output
RUN_OUTPUT=$(
  {
    echo "=== Run started: $(date) ==="
    bash "$WORK_DIR/run2.sh"
    echo "=== Run completed: $(date) ==="
  } 2>&1
)

# Build JSON payload for run log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
# Escape newlines and quotes in the output for a valid JSON string.
ESCAPED_RUN_OUTPUT=$(echo "$RUN_OUTPUT" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')
JSON_PAYLOAD=$(cat <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "run_log": "$ESCAPED_RUN_OUTPUT"
}
EOF
)

# Send the run log via webhook
sleep 3
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"

