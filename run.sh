#!/bin/bash

LOGFILE="log.txt"

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


# Copy log file into the repository
#cp "../$LOGFILE" .

# Commit and push
git add "$LOGFILE"
git commit -m "Add log from $(date)"
git push origin main