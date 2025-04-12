#!/bin/bash
# run2.sh

WORK_DIR="/home/spiesznikrysiek/Desktop/Chessbot/Chessbot_rasbpy"
WEBHOOK_URL="https://webhook.site/d3cb0112-da92-4eb2-8d12-0303bd957559"

cd "$WORK_DIR/Arduino" || { echo "Arduino directory not found"; exit 1; }

# Configure Arduino CLI
sudo ./arduino-cli config init --overwrite || { echo "Config initialization failed"; exit 1; }
sudo ./arduino-cli core update-index || { echo "Core index update failed"; exit 1; }
sudo ./arduino-cli core install arduino:avr || { echo "Core AVR installation failed"; exit 1; }
sudo ./arduino-cli core install arduino:megaavr || { echo "Core mega AVR installation failed"; exit 1; }

echo "Libraries installing."
sudo ./arduino-cli lib install "LiquidCrystal_I2C_Hangul" || { echo "LCD library installation failed"; exit 1; }
sudo ./arduino-cli lib install "AccelStepper" || { echo "AccelStepper library installation failed"; exit 1; }
sudo ./arduino-cli lib install "AccelStepperWithDistances" || { echo "AccelStepperWithDistances library installation failed"; exit 1; }
sudo ./arduino-cli lib install "Servo" || { echo "Servo library installation failed"; exit 1; }
echo "Libraries installed."

# Compile and upload the sketch
sudo ./arduino-cli compile --fqbn arduino:megaavr:nona4809 Arduino.ino || { echo "Compilation failed"; exit 1; }
echo "Waiting 20 seconds before attempting to upload the compiled sketch."
sleep 0
sudo ./arduino-cli upload -v -p /dev/ttyACM0 --fqbn arduino:megaavr:nona4809 . || { echo "Upload failed"; exit 1; }

echo "Arduino setup complete."
