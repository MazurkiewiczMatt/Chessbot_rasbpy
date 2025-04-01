#!/bin/bash

cd /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy



# Check if the directory was updated or not
if [[ $git_output == *"Already up to date."* ]]; then
    echo "The directory already has the latest version."
else
    echo "The directory was updated with the latest changes."
fi

# Install the required Python libraries
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip uninstall serial --break-system-packages
    pip install -r requirements.txt --break-system-packages
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

cd /home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy/Arduino || { echo "Arduino directory not found"; exit 1; }

# Configure Arduino CLI
sudo ./arduino-cli config init --overwrite || { echo "Config initialization failed"; exit 1; }
sudo ./arduino-cli core update-index || { echo "Core index update failed"; exit 1; }
sudo ./arduino-cli core install arduino:avr || { echo "Core AVR installation failed"; exit 1; }
sudo ./arduino-cli core install arduino:megaavr || { echo "Core mega AVR installation failed"; exit 1; }


sudo ./arduino-cli lib install "LiquidCrystal_I2C_Hangul" || { echo "LCD library installation failed"; exit 1; }
sudo ./arduino-cli lib install "AccelStepper" || { echo "AccelStepper library installation failed"; exit 1; }
sudo ./arduino-cli lib install "AccelStepperWithDistances" || { echo "AccelStepperWithDistances library installation failed"; exit 1; }
sudo ./arduino-cli lib install "Servo@1.2.2" || { echo "Servo library installation failed"; exit 1; }

# Compile and upload the sketch

sudo ./arduino-cli compile --fqbn arduino:megaavr:nona4809 Arduino.ino || { echo "Compilation failed"; exit 1; }
echo "Waiting 20 seconds before attempting to upload the compiled sketch."
sleep 20
sudo ./arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:megaavr:nona4809 . || { echo "Upload failed"; exit 1; }

echo "Arduino setup complete."

# Launch the Python script
