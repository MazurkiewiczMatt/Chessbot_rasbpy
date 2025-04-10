#!/bin/bash
WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"
WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"
ARDUINO_DIR="$WORK_DIR/Arduino"

# Checks
PING_INTERNET=$(ping -c 1 8.8.8.8 &>/dev/null && echo "OK" || echo "FAIL")
PING_GITHUB=$(ping -c 1 github.com &>/dev/null && echo "OK" || echo "FAIL")
MAIN_PY_EXISTS=$(test -f "$WORK_DIR/main.py" && echo "YES" || echo "NO")
ARDUINO_INO_EXISTS=$(test -f "$ARDUINO_DIR/Arduino.ino" && echo "YES" || echo "NO")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
ARDUINO_LIST=$(sudo "$WORK_DIR"/Arduino/arduino-cli board list)

# Prepare JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "internet": "$PING_INTERNET",
  "github": "$PING_GITHUB",
  "main_py_exists": "$MAIN_PY_EXISTS",
  "arduino_ino_exists": "$ARDUINO_INO_EXISTS",
  "arduino_list": "$ARDUINO_LIST"
}
EOF
)

# Send JSON data via cURL
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"
