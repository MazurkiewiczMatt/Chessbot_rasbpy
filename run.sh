#!/bin/bash

cd /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy

# Pull latest changes and reset
find .git/objects/ -size 0 -exec rm -f {} \;
git fetch origin
git pull
git reset --hard origin/main

# Create log file with basic timestamp
LOGFILE="log-$(date +%Y%m%d-%H%M%S).txt"
touch "$LOGFILE"

# Initial commit with empty log
git add "$LOGFILE"
git commit -m "Empty log created"
git push origin main

# Execute and log run2.sh
chmod +x run2.sh
{
    echo "=== Run started: $(date) ==="
    ./run2.sh
    echo "=== Run completed: $(date) ==="
} &> "$LOGFILE"

# Final commit with actual log
git add "$LOGFILE"
git commit -m "Log from $(date +%Y%m%d-%H%M%S)"
git push origin main

# Launch main application
python3 /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy/main.py