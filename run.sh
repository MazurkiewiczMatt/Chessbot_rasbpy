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
    pip uninstall serial
    pip install -r requirements.txt --break-system-packages
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

cd /home/artur/Chessbot_rasbpy/Arduino || { echo "Arduino directory not found"; exit 1; }

# Configure Arduino CLI
sudo ./arduino-cli config init --overwrite || { echo "Config initialization failed"; exit 1; }
sudo ./arduino-cli core update-index || { echo "Core index update failed"; exit 1; }
sudo ./arduino-cli core install arduino:avr || { echo "Core installation failed"; exit 1; }

# Compile and upload the sketch

sudo ./arduino-cli compile --fqbn arduino:avr:nano . || { echo "Compilation failed"; exit 1; }
sudo ./arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:nano . || { echo "Upload failed"; exit 1; }

echo "Arduino setup complete."

# Launch the Python script
python3 /home/artur/Chessbot_rasbpy/main.py
