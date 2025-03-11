#!/bin/bash

cd /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy

# Pull the latest changes from the git repository
find .git/objects/ -size 0 -exec rm -f {} \;
git fetch origin
git_output=$(git pull)
git reset --hard origin/main

TIMESTAMP=$(date +%Y%m%d%H%M%S)
LOGFILE="log-${TIMESTAMP}.txt"

# Ensure log file is created
touch "$LOGFILE"
git add "$LOGFILE"
git commit . -m "empty log from $(date +%Y%m%d%H%M%S)"
git push origin main

# Make run2.sh executable
chmod +x run2.sh
echo "run2.sh START"
# Capture output of run2.sh into the log file
{
    echo "=== Starting run2.sh at $(date) ==="
    ./run2.sh
    echo "=== Finished run2.sh at $(date) ==="
} &> "$LOGFILE" 

echo "run2.sh ENDING"

# Copy log file into the repository
echo "cp logfile start"
cp "../$LOGFILE" .
echo "cp logfile end"
# Commit and push
git commit . -m "Add log from $(TIMESTAMP)"
git push origin main
python3 /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy/main.py