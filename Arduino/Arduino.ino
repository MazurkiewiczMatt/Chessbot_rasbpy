#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

#define motorInterfaceType AccelStepper::DRIVER

// Create instances for two steppers, LCD, and servo.
AccelStepper stepper1(motorInterfaceType, 3, 2);
AccelStepper stepper2(motorInterfaceType, 5, 4);
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

// Function to update the LCD display.
void displayLCD(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

// Parse and handle LCD commands (format: "LCD first line, second line").
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

// Move both steppers by given steps.
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

// Extract step values from a command string (format: "MOVE step1 step2").
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

void setup() {
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
  moveSteppers(50,-50);
  // Initialize servo (set a default starting position).
  myservo.attach(6);
  myservo.write(30);
  Serial.println("Basic Chessbot initiated");
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();
    if (message.equalsIgnoreCase("PING")) {
      Serial.println("PONG");
    } else if (message.startsWith("LCD")) {
      handleLCDCommand(message.substring(3));
    } else if (message.startsWith("MOVE")) {
      handleMoveCommand(message.substring(4));
    } else {
      Serial.println("Unknown command");
    }
  }
}
