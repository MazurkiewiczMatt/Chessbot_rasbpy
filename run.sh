#!/bin/bash

cd /home/artur/Chessbot_rasbpy

# Pull the latest changes from the git repository
git_output=$(git pull)

# Check if the directory was updated or not
if [[ $git_output == *"Already up to date."* ]]; then
    echo "The directory already has the latest version."
else
    echo "The directory was updated with the latest changes."
fi

# Install the required Python libraries
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt --break-system-packages
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Launch the Python script
python3 /home/artur/Chessbot_rasbpy/main.py
