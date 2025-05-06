#!/bin/bash
# update.sh

# Get the session identifier from the first argument, defaulting to "unknown" if missing
SESSION_ID=${1:-"unknown"}

WEBHOOK_URL="https://webhook.site/b515c902-f0a9-497e-834e-ee60d14b2450"
WORK_DIR="/home/pi/chessbot/Chessbot_rasbpy"

# Change to working directory
cd "$WORK_DIR" || exit 1

# Clean up zero-size git object files
clean_output=$(find .git/objects/ -size 0 -exec rm -f {} \; 2>&1)

# Perform Git operations and capture their full output
git_fetch_output=$(git fetch origin 2>&1)
git_pull_output=$(git pull 2>&1)
git_reset_output=$(git reset --hard origin/main 2>&1)

# Determine update status based on the git pull output
if [[ $git_pull_output == *"Already up to date."* ]]; then
    UPDATE_STATUS="The directory already has the latest version."
else
    UPDATE_STATUS="The directory was updated with the latest changes."
fi

# Dependency installation status
DEP_STATUS=""

# Install tkinter using apt
DEP_STATUS+="Installing tkinter using apt...\n"
tk_install_output=$(sudo apt-get update && sudo apt-get install -y python3-tk 2>&1)
DEP_STATUS+="tkinter install output:\n$tk_install_output\n"

# Install pip dependencies if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    DEP_STATUS+="Installing pip dependencies from requirements.txt...\n"
    pip3 uninstall serial --break-system-packages > /dev/null 2>&1
    pip_install_output=$(pip3 install -r requirements.txt --break-system-packages 2>&1)
    DEP_STATUS+="pip install output:\n$pip_install_output"
else
    DEP_STATUS+="requirements.txt not found. Skipping pip dependency installation."
fi

# Get the current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Escape JSON payload properly
ESCAPED_DEP_STATUS=$(echo "$DEP_STATUS" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')

# Prepare JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "update_status": "$UPDATE_STATUS",
  "git": {
    "clean_output": "$clean_output",
    "fetch_output": "$git_fetch_output",
    "pull_output": "$git_pull_output",
    "reset_output": "$git_reset_output"
  },
  "dependency_status": "$ESCAPED_DEP_STATUS"
}
EOF
)

# Send JSON data via cURL to the webhook
sleep 3
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"
