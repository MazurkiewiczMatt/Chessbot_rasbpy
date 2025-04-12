#!/bin/bash
# run.sh

# Generate a unique session identifier (requires uuidgen to be installed)
SESSION_ID=$(uuidgen)

# Define environment variables
WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"
WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"

# Run diagnostics first
chmod +x "$WORK_DIR/diagnostic.sh"
"$WORK_DIR/diagnostic.sh" "$SESSION_ID"

chmod +x "$WORK_DIR/enable_ssh.sh"
"$WORK_DIR/enable_ssh.sh" "$SESSION_ID"

chmod +x "$WORK_DIR/update.sh"
"$WORK_DIR/update.sh" "$SESSION_ID"

chmod +x "$WORK_DIR/arduino.sh"
"$WORK_DIR/arduino.sh" "$SESSION_ID"

python3 "$WORK_DIR/main.py"
