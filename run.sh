#!/bin/bash
# run.sh

# Define environment variables
WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"
WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"

# Run diagnostics first
chmod +x "$WORK_DIR/diagnostic.sh"
"$WORK_DIR/diagnostic.sh"

chmod +x "$WORK_DIR/enable_ssh.sh"
"$WORK_DIR/enable_ssh.sh"

chmod +x "$WORK_DIR/update.sh"
"$WORK_DIR/update.sh"

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
  "timestamp": "$TIMESTAMP",
  "run_log": "$ESCAPED_RUN_OUTPUT"
}
EOF
)

# Send the run log via webhook
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"

# Launch the main application
python3 "$WORK_DIR/main.py"
