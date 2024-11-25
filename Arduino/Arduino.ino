#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

// Define motor interface type
#define motorInterfaceType AccelStepper::DRIVER

// Initialize stepper motors with appropriate pins
AccelStepper stepper1(motorInterfaceType, 3, 2); // Stepper1 (Step, Dir)
AccelStepper stepper2(motorInterfaceType, 5, 4); // Stepper2 (Step, Dir)

// Initialize the LCD with the I2C address (usually 0x27 or 0x3F)
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

// Define homing button pins
const int homeButton1Pin = 7; // Button for Stepper1 Homing
const int homeButton2Pin = 8; // Button for Stepper2 Homing

// Debounce variables to prevent multiple triggers
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
const unsigned long debounceDelay = 50;

// Homing step size
const int homingSteps = 5000;

// Function to display messages on LCD
void displayLCD(String line1, String line2) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(line1);
    lcd.setCursor(0, 1);
    lcd.print(line2);
}

// Function to move steppers
void moveSteppers(int step1, int step2) {
    // Set the target positions for both steppers
    stepper1.move(step1);
    stepper2.move(step2);

    Serial.print("Moving Stepper1 by ");
    Serial.print(step1);
    Serial.print(" steps and Stepper2 by ");
    Serial.print(step2);
    Serial.println(" steps.");

    // Continue running the motors until both have completed their moves
    while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
        stepper1.run();
        stepper2.run();
    }

    Serial.println("Steppers movement completed.");
}

// Function to handle LCD command
void handleLCDCommand(String lcdData) {
    // Split the lcdData by comma
    int commaIndex = lcdData.indexOf(',');
    if (commaIndex != -1) {
        String line1 = lcdData.substring(0, commaIndex);
        line1.trim(); // Trim leading and trailing whitespace

        String line2 = lcdData.substring(commaIndex + 1);
        line2.trim(); // Trim leading and trailing whitespace

        Serial.println("LCD SUCCESS");
        displayLCD(line1, line2); // Use dedicated LCD display function
    } else {
        Serial.println("LCD command format error. Use: LCD first line, second line");
    }
}

// Function to handle MOVE command
void handleMoveCommand(String moveData) {
    // Example expected format: "MOVE 100 500"
    // We'll parse two integers separated by space

    moveData.trim(); // Remove any leading/trailing whitespace

    // Find the first space after "MOVE"
    int firstSpace = moveData.indexOf(' ');
    if (firstSpace == -1) {
        Serial.println("MOVE command format error. Use: MOVE step1 step2");
        return;
    }

    // Extract the substring after the first space
    String stepsStr = moveData.substring(firstSpace + 1);
    stepsStr.trim(); // Trim whitespace

    // Find the space between step1 and step2
    int secondSpace = stepsStr.indexOf(' ');
    if (secondSpace == -1) {
        Serial.println("MOVE command format error. Use: MOVE step1 step2");
        return;
    }

    // Extract step1 and step2 as strings
    String step1Value = stepsStr.substring(0, secondSpace);
    step1Value.trim();

    String step2Value = stepsStr.substring(secondSpace + 1);
    step2Value.trim();

    // Convert the step strings to integers
    int step1 = step1Value.toInt();
    int step2 = step2Value.toInt();

    // Basic validation to ensure that the conversion was successful
    if ((step1Value.length() == 0) || (step2Value.length() == 0)) {
        Serial.println("Invalid step values. Ensure both step1 and step2 are integers.");
        return;
    }

    // Move the steppers according to the steps provided
    moveSteppers(step1, step2);

    // Update LCD with movement status
    displayLCD("Motors Moving", "Step1: " + String(step1) + " Step2: " + String(step2));

    Serial.print("STEPPERS MOVED: ");
    Serial.print(step1);
    Serial.print(", ");
    Serial.println(step2);
}

// Function to perform homing for a stepper
void performHoming(AccelStepper& stepper, bool initialDirectionPositive, int buttonPin, String stepperName) {
    // Start moving in initial direction
    displayLCD("Homing " + stepperName, initialDirectionPositive ? "Moving Positive" : "Moving Negative");
    Serial.println("Homing " + stepperName + ": Moving " + (initialDirectionPositive ? "Positive" : "Negative") + " direction.");

    // Move stepper in the initial direction indefinitely (or a very large number)
    stepper.move(initialDirectionPositive ? 1000000 : -1000000); // Adjust as needed

    // Run the stepper until the homing button is pressed
    while (stepper.distanceToGo() != 0) {
        stepper.run();

        if (digitalRead(buttonPin) == LOW) { // Button pressed
            // Debounce
            unsigned long currentTime = millis();
            if (stepperName == "Stepper1") {
                if (currentTime - lastDebounceTime1 > debounceDelay) {
                    lastDebounceTime1 = currentTime;
                } else {
                    continue; // Ignore if within debounce delay
                }
            } else if (stepperName == "Stepper2") {
                if (currentTime - lastDebounceTime2 > debounceDelay) {
                    lastDebounceTime2 = currentTime;
                } else {
                    continue; // Ignore if within debounce delay
                }
            }

            // Stop stepper immediately
            stepper.stop();
            displayLCD("Homing " + stepperName, "Stopping...");
            Serial.println("Button pressed. Stopping " + stepperName + ".");

            break; // Exit the homing loop
        }
    }

    // Move back 5000 steps in the opposite direction
    displayLCD("Homing " + stepperName, "Moving back 5000 steps");
    Serial.println("Homing " + stepperName + ": Moving back 5000 steps in opposite direction.");
    stepper.move(initialDirectionPositive ? -homingSteps : homingSteps);

    // Run the stepper until movement is complete
    while (stepper.distanceToGo() != 0) {
        stepper.run();
    }

    // Set current position to 0
    stepper.setCurrentPosition(0);
    displayLCD(stepperName + " Homed", "");
    Serial.println(stepperName + " homed to position 0.");
}

// Function to perform homing sequence for both steppers
void homeAllSteppers() {
    Serial.println("Initiating homing sequence.");
    displayLCD("Homing Initiated", "");

    // Homing Stepper1: initial direction positive, button pin7
    performHoming(stepper1, true, homeButton1Pin, "Stepper1");

    // Homing Stepper2: initial direction negative, button pin8
    performHoming(stepper2, false, homeButton2Pin, "Stepper2");

    // Homing complete
    displayLCD("Homing Complete", "");
    Serial.println("Homing sequence completed.");
}

void setup() {
    // Initialize button pins with internal pull-up resistors
    pinMode(homeButton1Pin, INPUT_PULLUP);
    pinMode(homeButton2Pin, INPUT_PULLUP);

    Wire.begin();
    Serial.begin(9600); // Begin serial communication
    Serial.setTimeout(100); // Increased timeout for better message reception
    Serial.println("Chessbot software initiated");

    // Initialize the LCD
    Serial.print("Initializing LCD...");
    lcd.init();
    lcd.backlight(); // Turn on the backlight
    displayLCD("INITIALIZED", "v2");
    Serial.println(" Initialized LCD successfully");

    // Initialize stepper motors
    stepper1.setMaxSpeed(1000); // Set max speed for Stepper1
    stepper1.setAcceleration(500); // Set max acceleration for Stepper1
    stepper2.setMaxSpeed(1000); // Set max speed for Stepper2
    stepper2.setAcceleration(500); // Set max acceleration for Stepper2
}

void loop() {
    // Handle serial commands
    if (Serial.available() > 0) {
        String message = Serial.readStringUntil('\n');
        message.trim(); // Remove any leading/trailing whitespace or newline characters

        // Serial.print("Received message: ");
        // Serial.println(message);

        // Respond to PING
        if (message.equalsIgnoreCase("PING")) {
            Serial.println("PONG");

        // Handle LCD message
        } else if (message.startsWith("LCD")) {
            String lcdData = message.substring(3); // Extract data after "LCD"
            lcdData.trim(); // Trim whitespace
            handleLCDCommand(lcdData);

        // Handle MOVE command
        } else if (message.startsWith("MOVE")) {
            handleMoveCommand(message);

        // Handle HOME command
        } else if (message.equalsIgnoreCase("HOME")) {
            homeAllSteppers();
        } else {
            Serial.println("Unknown command");
        }
    }
}
