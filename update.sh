#!/bin/bash
# update.sh

WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"
WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"

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

# Install the required Python libraries if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    DEP_STATUS="Installing dependencies from requirements.txt. "
    pip uninstall serial --break-system-packages > /dev/null 2>&1
    pip_install_output=$(pip install -r requirements.txt --break-system-packages 2>&1)
    DEP_STATUS+="Dependencies installation output: ${pip_install_output}"
else
    DEP_STATUS="requirements.txt not found. Skipping dependency installation."
fi

# Get the current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Prepare JSON payload with all Git outputs and dependency status
JSON_PAYLOAD=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "update_status": "$UPDATE_STATUS",
  "git": {
    "clean_output": "$clean_output",
    "fetch_output": "$git_fetch_output",
    "pull_output": "$git_pull_output",
    "reset_output": "$git_reset_output"
  },
  "dependency_status": "$DEP_STATUS"
}
EOF
)

# Send JSON data via cURL to the webhook
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD"
