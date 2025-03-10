#!/bin/bash

# Pull the latest changes from the git repository
find .git/objects/ -size 0 -exec rm -f {} \;
git fetch origin
git_output=$(git pull)
git reset --hard origin/main

LOGFILE="log.txt"
sudo rm "$LOGFILE"
# Ensure log file exists
touch "$LOGFILE"

# Make run2.sh executable
chmod +x run2.sh

# Capture output of run2.sh into the log file
{
    echo "=== Starting run2.sh at $(date) ==="
    ./run2.sh
    echo "=== Finished run2.sh at $(date) ==="
} &> "$LOGFILE" 


# Copy log file into the repository
cp "../$LOGFILE" .

# Commit and push
git commit . -m "Add log from $(date)"
git push origin main
python3 /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy/main.py