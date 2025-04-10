#!/bin/bash
# run.sh

# Define environment variables
WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"
WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"

# Run diagnostics first
chmod +x "$WORK_DIR/diagnostic.sh"
"$WORK_DIR/diagnostic.sh"

# Change to working directory and update repository
cd "$WORK_DIR" || exit 1
find .git/objects/ -size 0 -exec rm -f {} \;
git fetch origin
git pull
git reset --hard origin/main
sleep 5

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

# Wait before launching the main application
sleep 500

# Launch the main application
python3 "$WORK_DIR/main.py"
