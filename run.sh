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

# Check if arduino-cli is installed
if ! command -v arduino-cli &> /dev/null; then
    echo "arduino-cli not found. Installing..."

    # Download and install arduino-cli
    wget https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linuxarm.tar.gz || { echo "Download failed"; exit 1; }
    tar -xvf arduino-cli_latest_Linuxarm.tar.gz || { echo "Failed to extract"; exit 1; }
    sudo mv arduino-cli /usr/local/bin/ || { echo "Failed to move arduino-cli"; exit 1; }
else
    echo "arduino-cli is already installed."
fi

# Configure Arduino CLI
arduino-cli config init || { echo "Config initialization failed"; exit 1; }
arduino-cli core update-index || { echo "Core index update failed"; exit 1; }
arduino-cli core install arduino:avr || { echo "Core installation failed"; exit 1; }

# Compile and upload the sketch
cd /home/artur/Chessbot_rasbpy/Arduino || { echo "Sketch directory not found"; exit 1; }
arduino-cli compile --fqbn arduino:avr:nano . || { echo "Compilation failed"; exit 1; }
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:nano . || { echo "Upload failed"; exit 1; }

echo "Arduino setup complete."

# Launch the Python script
python3 /home/artur/Chessbot_rasbpy/main.py
