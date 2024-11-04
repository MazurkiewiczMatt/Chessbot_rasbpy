#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

#define motorInterfaceType AccelStepper::DRIVER

AccelStepper stepper1(motorInterfaceType, 3, 2); // Pins for stepper 1
AccelStepper stepper2(motorInterfaceType, 5, 4); // Pins for stepper 2

// Initialize the LCD with the I2C address (usually 0x27 or 0x3F)
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

String lcdMessage = "";  // Variable to store the text after LCD

void setup() {
  Wire.begin();
  Serial.begin(9600); // Begin serial communication
  Serial.setTimeout(20);
  Serial.println("Chessbot software initiated");

  // Initialize the LCD
  Serial.print("Initializing LCD");
  lcd.init();
  lcd.backlight(); // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("INITIALIZED");
  Serial.print("Initialized LCD successfully");

  // Initialize stepper motors
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(500);
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(500);
}

void moveSteppers(int steps1[], int steps2[], int size) {
  for (int i = 0; i < size; i++) {
    stepper1.move(steps1[i]);
    stepper2.move(steps2[i]);

    // Continue running the motors until both have completed their moves
    while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
      stepper1.run();
      stepper2.run();
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');

    // Respond to PING
    if (message == "PING") {
      Serial.println("PONG");

    // Handle LCD message
    } else if (message.startsWith("LCD")) {
      lcdMessage = message.substring(4);  // Save the text after "LCD " into lcdMessage
      Serial.print("LCD SUCCESS");
      lcd.clear(); // Clear the LCD
      lcd.setCursor(0, 0); // Set cursor to the top left
      lcd.print(lcdMessage); // Print the received data on the LCD

    // Handle stepper motor command
    } else if (message.startsWith("MOVE")) {
      // Extract the step values from the message
      int steps1[] = { /* populate with appropriate values based on your needs */ };
      int steps2[] = { /* populate with appropriate values based on your needs */ };
      int numSteps = sizeof(steps1) / sizeof(steps1[0]);

      // Move the steppers according to the steps provided
      moveSteppers(steps1, steps2, numSteps);

      // Update LCD with movement status
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Motors Moving");

      Serial.print("STEPPERS MOVED");
    }
  }
}
