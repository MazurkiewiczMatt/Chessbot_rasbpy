#!/bin/bash

LOGFILE="log.txt"
REPO_DIR="log-repo"  # Directory for the repository

# Ensure log file exists
touch "$LOGFILE"

# Make run2.sh executable
chmod +x run2.sh

# Capture output of run2.sh into the log file
{
    echo "=== Starting run2.sh at $(date) ==="
    ./run2.sh
    echo "=== Finished run2.sh at $(date) ==="
} >> "$LOGFILE" 2>&1

# Install GitHub CLI and git
sudo apt update && sudo apt install gh git -y

# Authenticate with GitHub (replace token)

# Clone or initialize the repository
if [ -d "$REPO_DIR" ]; then
    cd "$REPO_DIR"
    git pull
else
    gh repo create "log-repo" --public --confirm
    git clone "https://github.com/yourusername/log-repo.git" "$REPO_DIR"
    cd "$REPO_DIR"
fi

# Copy log file into the repository
cp "../$LOGFILE" .

# Commit and push
git add "$LOGFILE"
git commit -m "Add log from $(date)"
git push origin main