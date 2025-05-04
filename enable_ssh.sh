#!/bin/bash
# enable_ssh_log.sh
#
# This script assumes your Raspberry Pi is already connected to WiFi.
# It performs the following:
#   - Checks WiFi connectivity by determining the IP address on wlan0.
#   - Pings 8.8.8.8 to verify internet connectivity.
#   - Enables and starts the SSH service.
#   - Logs relevant diagnostic information to a specified webhook.
#
# Usage:
#   chmod +x enable_ssh_log.sh
#   sudo ./enable_ssh_log.sh

# Get the session identifier from the first argument, defaulting to "unknown" if missing
SESSION_ID=${1:-"unknown"}


# --- Configuration ---
WEBHOOK_URL="https://webhook.site/b515c902-f0a9-497e-834e-ee60d14b2450"

# --- Gather Timestamp ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# --- Check WiFi Connectivity ---
WIFI_IP=$(ip a show wlan0 | awk '/inet / {print $2}' | cut -d/ -f1)

if [ -z "$WIFI_IP" ]; then
    WIFI_STATUS="FAIL"
    echo "No WiFi connection detected on interface wlan0. Exiting."
    # Prepare JSON payload for logging before exiting.
    JSON_PAYLOAD=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "wifi_status": "$WIFI_STATUS",
  "wlan_ip": "NONE"
}
EOF
)
    curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"
    exit 1
else
    WIFI_STATUS="OK"
    echo "WiFi is connected. IP address: $WIFI_IP"
fi

# --- Test Internet Connectivity ---
PING_INTERNET=$(ping -c 1 8.8.8.8 &>/dev/null && echo "OK" || echo "FAIL")
echo "Internet connectivity check: $PING_INTERNET"

# --- Enable and Start SSH Service ---
echo "Enabling and starting SSH service..."
sudo systemctl enable ssh
sudo systemctl start ssh

# --- Check SSH Service Status ---
SSH_STATUS=$(systemctl is-active ssh)
echo "SSH service status: $SSH_STATUS"

# --- Prepare JSON Payload for Logging ---
JSON_PAYLOAD=$(cat <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "wifi_status": "$WIFI_STATUS",
  "wlan_ip": "$WIFI_IP",
  "ping_internet": "$PING_INTERNET",
  "ssh_status": "$SSH_STATUS"
}
EOF
)

echo "Logging diagnostic information:"
echo "$JSON_PAYLOAD"

# --- Send the Diagnostic Information via cURL ---
sleep 3
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"

# --- Final User Message ---
echo "SSH is now accessible on your Raspberry Pi. Connect using:"
echo "ssh pi@$WIFI_IP"

exit 0
