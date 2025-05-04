#!/bin/bash
# run.sh

LOCKFILE="/tmp/run_sh.lock"
SUCCESS_MARKER="/home/pi/.chessbot_success"
WEBHOOK_URL="https://webhook.site/b515c902-f0a9-497e-834e-ee60d14b2450"
WORK_DIR="/home/pi/chessbot/Chessbot_rasbpy"

# If already succeeded before, skip execution
if [ -f "$SUCCESS_MARKER" ]; then
    echo "run.sh has already completed successfully. Skipping."
    exit 0
fi

# Prevent concurrent execution
if [ -e "${LOCKFILE}" ]; then
    echo "Script is already running. DUPLICATE"
    exit 1
fi

trap "rm -f ${LOCKFILE}" EXIT
touch ${LOCKFILE}

ps aux | grep run.sh

# Generate a unique session identifier (requires uuidgen to be installed)
echo "Generating session ID..."
SESSION_ID=$(uuidgen)
echo "Session ID: $SESSION_ID"

# Run diagnostics first
echo "Preparing to run diagnostic.sh..."
chmod +x "$WORK_DIR/diagnostic.sh"
echo "Running diagnostic.sh with session ID: $SESSION_ID"
"$WORK_DIR/diagnostic.sh" "$SESSION_ID" || exit 1

# Enable SSH
echo "Preparing to run enable_ssh.sh..."
chmod +x "$WORK_DIR/enable_ssh.sh"
echo "Running enable_ssh.sh with session ID: $SESSION_ID"
"$WORK_DIR/enable_ssh.sh" "$SESSION_ID" || exit 1

# Pull latest code & install dependencies
echo "Preparing to run update.sh..."
chmod +x "$WORK_DIR/update.sh"
echo "Running update.sh with session ID: $SESSION_ID"
"$WORK_DIR/update.sh" "$SESSION_ID" || exit 1

# Run Arduino upload/setup
echo "Preparing to run arduino.sh..."
chmod +x "$WORK_DIR/arduino.sh"
echo "Running arduino.sh with session ID: $SESSION_ID"
"$WORK_DIR/arduino.sh" "$SESSION_ID" || exit 1

# Launch Python main script
echo "Launching main.py with Python3..."
python3 "$WORK_DIR/main.py" || exit 1

# If we got here, all steps succeeded — mark success
echo "run.sh completed successfully. Marking as complete."
touch "$SUCCESS_MARKER"
