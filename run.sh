#!/bin/bash

# Pull the latest changes from the git repository
git_output=$(git pull)

# Check if the directory was updated or not
if [[ $git_output == *"Already up to date."* ]]; then
    echo "The directory already has the latest version."
else
    echo "The directory was updated with the latest changes."
fi

# Launch the Python script
python3 main.py
