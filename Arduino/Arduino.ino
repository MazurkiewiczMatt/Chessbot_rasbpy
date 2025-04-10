#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

#define motorInterfaceType AccelStepper::DRIVER

// Define stepper motor instances.
AccelStepper stepper1(motorInterfaceType, 3, 2);
AccelStepper stepper2(motorInterfaceType, 5, 4);

// Define the LCD instance.
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);

// Home button pins and debounce settings.
const int homeButton1Pin = 7;
const int homeButton2Pin = 8;
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
const unsigned long debounceDelay = 50;
const int homingSteps = 5000;

// Waiting messages and connection flag.
bool Connected = false;
bool ranTest = false;
const char* messages[][2] = {
  {"1234567890123456", "1234567890123456"},
  {"revving chess", "engine"},
  {"inferring piece", "locations"},
  {"plotting", "check mate"}
};
const int numMessages = sizeof(messages) / sizeof(messages[0]);
unsigned long waitingStartTime = 0;
unsigned long lastMessageTime = 0;

//
// Utility Functions
//

// Display two lines on the LCD.
void displayLCD(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

// Parse and execute an LCD command with comma separation.
void handleLCDCommand(String lcdData) {
  int commaIndex = lcdData.indexOf(',');
  if (commaIndex != -1) {
    String line1 = lcdData.substring(0, commaIndex);
    line1.trim();
    String line2 = lcdData.substring(commaIndex + 1);
    line2.trim();
    displayLCD(line1, line2);
    Serial.println("LCD SUCCESS");
  } else {
    Serial.println("LCD command format error. Use: LCD first line, second line");
  }
}

// Move both steppers with given step counts.
void moveSteppers(int step1, int step2) {
  stepper1.move(step1);
  stepper2.move(step2);
  while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
  }
  Serial.print("STEPPERS MOVED: ");
  Serial.print(step1);
  Serial.print(", ");
  Serial.println(step2);
}

// Handle MOVE command (expects "MOVE step1 step2").
void handleMoveCommand(String moveData) {
  moveData.trim();
  int firstSpace = moveData.indexOf(' ');
  if (firstSpace == -1) {
    Serial.println("MOVE command format error. Use: MOVE step1 step2");
    return;
  }
  String stepsStr = moveData.substring(firstSpace + 1);
  stepsStr.trim();
  int secondSpace = stepsStr.indexOf(' ');
  if (secondSpace == -1) {
    Serial.println("MOVE command format error. Use: MOVE step1 step2");
    return;
  }
  String step1Value = stepsStr.substring(0, secondSpace);
  step1Value.trim();
  String step2Value = stepsStr.substring(secondSpace + 1);
  step2Value.trim();
  int step1 = step1Value.toInt();
  int step2 = step2Value.toInt();
  if (step1Value.length() == 0 || step2Value.length() == 0) {
    Serial.println("Invalid step values. Ensure both step1 and step2 are integers.");
    return;
  }
  moveSteppers(step1, step2);
  displayLCD("Motors Moving", "Step1:" + String(step1) + " Step2:" + String(step2));
}

//
// Homing Functions
//

// Perform homing routine for a single stepper.
void performHoming(AccelStepper &stepper, bool initialDirectionPositive, int buttonPin1, int buttonPin2, String stepperName) {
  float origMaxSpeed = stepper.maxSpeed();
  // Lower speed for homing.
  stepper.setMaxSpeed(30);

  displayLCD("Homing " + stepperName, (initialDirectionPositive ? "Moving +ve" : "Moving -ve"));
  stepper.move(initialDirectionPositive ? 1000000 : -1000000);
  unsigned long *lastDebounceTime = (stepperName == "Stepper1") ? &lastDebounceTime1 : &lastDebounceTime2;

  while (stepper.distanceToGo() != 0) {
    stepper.run();
    if (digitalRead(buttonPin1) == LOW || digitalRead(buttonPin2) == LOW) {
      unsigned long now = millis();
      if (now - *lastDebounceTime > debounceDelay) {
        *lastDebounceTime = now;
        stepper.stop();
        displayLCD("Homing " + stepperName, "Stopping...");
        break;
      }
    }
  }

  displayLCD("Homing " + stepperName, "Moving back 5000");
  stepper.move(initialDirectionPositive ? -homingSteps : homingSteps);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }

  displayLCD("Homing " + stepperName, "Offsetting 30");
  stepper.move(initialDirectionPositive ? 30 : -30);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }

  stepper.setCurrentPosition(0);
  stepper.setMaxSpeed(origMaxSpeed);

  displayLCD(stepperName + " Homed", "");
}

// Home both steppers.
void homeAllSteppers() {
  displayLCD("Homing Initiated", "");
  performHoming(stepper1, true, homeButton1Pin, homeButton2Pin, "Stepper1");
  performHoming(stepper2, false, homeButton1Pin, homeButton2Pin, "Stepper2");
  displayLCD("Homing Complete", "");
  Serial.println("Homing sequence complete.");
}

//
// Waiting Display Routine
//

// While waiting for a connection, cycle through messages and time out after 90 seconds.
void waitingDisplay() {
  if (waitingStartTime == 0) {
    waitingStartTime = millis();
  }
  const unsigned long timeoutMillis = 90000; // 90 seconds
  unsigned long elapsedMillis = millis() - waitingStartTime;

  if (elapsedMillis >= timeoutMillis) {
    displayLCD("90s Mark:", "No Connection");
    waitingStartTime = millis(); // reset timer
    return;
  }

  if (millis() - lastMessageTime >= 5000) { // update every 5 seconds
    int messageIndex = random(numMessages);
    displayLCD(messages[messageIndex][0], messages[messageIndex][1]);
    lastMessageTime = millis();
  }

  // Check for any serial input to flag connection.
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();
    if (message.length() > 0) {
      Connected = true;
      displayLCD("Connection", "Established!");
      delay(2000);
    }
  }
}

//
// Setup and Main Loop
//

void setup() {
  // Initialize home buttons.
  pinMode(homeButton1Pin, INPUT_PULLUP);
  pinMode(homeButton2Pin, INPUT_PULLUP);
  Serial.begin(9600);
  Serial.setTimeout(100);
  lcd.init();
  lcd.backlight();
  displayLCD("System", "Initialized");

  // Configure steppers.
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(500);
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(500);

  // Seed random generator.
  randomSeed(analogRead(0));

  Serial.println("Chessbot Software Initiated (No Servo)");
}

void loop() {
  if (!Connected) {
    waitingDisplay();
  } else {
    if (!ranTest) {
      // Run a one-time test sequence upon connection.
      displayLCD("20 APRIL", "10 104");
      delay(10000);  // 10-second delay.
      homeAllSteppers();
      ranTest = true;
      delay(10000);
    }
    if (Serial.available() > 0) {
      String message = Serial.readStringUntil('\n');
      message.trim();
      if (message.equalsIgnoreCase("PING")) {
        Serial.println("PONG");
      } else if (message.startsWith("LCD")) {
        handleLCDCommand(message.substring(3));
      } else if (message.startsWith("MOVE")) {
        handleMoveCommand(message.substring(4));
      } else if (message.equalsIgnoreCase("HOME")) {
        homeAllSteppers();
      } else {
        Serial.println("Unknown command");
      }
    }
  }
}
