#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

#define motorInterfaceType AccelStepper::DRIVER

// Define stepper motors and their control pins
AccelStepper stepper1(motorInterfaceType, 3, 2); // Stepper 1 pins (step, dir)
AccelStepper stepper2(motorInterfaceType, 5, 4); // Stepper 2 pins (step, dir)

// Define limit switch pins
const int limitSwitch1 = 7;  // Limit switch for stepper1
const int limitSwitch2 = 8;  // Limit switch for stepper2

// Initialize the LCD with the I2C address
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

String lcdMessage = "";  // Variable to store text for the LCD

void setup() {
  Wire.begin();
  Serial.begin(9600); // Begin serial communication
  Serial.setTimeout(20);
  Serial.println("Chessbot software initiated");

  // Initialize the LCD
  Serial.println("Initializing LCD");
  lcd.init();
  lcd.backlight(); // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("INITIALIZED");
  Serial.println("Initialized LCD successfully");

  // Set pin modes for limit switches
  pinMode(limitSwitch1, INPUT_PULLUP);
  pinMode(limitSwitch2, INPUT_PULLUP);

  // Initialize stepper motors
  stepper1.setMaxSpeed(20000);
  stepper1.setAcceleration(60000);
  stepper2.setMaxSpeed(20000);
  stepper2.setAcceleration(60000);

  // Perform homing sequence
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Homing...");
  

  homeStepper(stepper1, limitSwitch2, -500000);  // Homing stepper1 towards limitSwitch2
  stepper1.setCurrentPosition(0);             

  moveStepper(stepper1, -12400); 
  stepper1.setCurrentPosition(0);       

  homeStepper(stepper2, limitSwitch1, 500000); // Homing stepper2 towards limitSwitch1
  stepper2.setCurrentPosition(0);             // Reset position to 0 after move

  moveStepper(stepper2, 12400);    // Move stepper2 1000 steps in opposite direction
  stepper2.setCurrentPosition(0);             // Reset position to 0 after move

  lcd.clear();
  
  lcd.setCursor(0, 0);
  lcd.print("Homing done");
  lcd.setCursor(0, 1);
  lcd.print("Standby");
}

// Function to home a stepper motor until a limit switch is pressed
void homeStepper(AccelStepper& stepper, int limitSwitchPin, int homingSpeed) {
  stepper.setSpeed(homingSpeed);  // Move in the homing direction
  while (digitalRead(limitSwitchPin) == HIGH) {
    stepper.runSpeed();
  }
  stepper.stop();
  Serial.print("Stepper homed on switch ");
  Serial.println(limitSwitchPin);
}

// Function to move a stepper motor along a trajectory
void moveStepper(AccelStepper& stepper, int steps) {
  stepper.move(steps);  // Move stepper by the specified steps

  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}

void loop() {
  if((digitalRead(limitSwitch2) == LOW)){
        lcd.setCursor(0, 0);
        lcd.print("B1");
        }
    if((digitalRead(limitSwitch1) == LOW)){
        lcd.setCursor(0, 0);
        lcd.print("B2");
        }

  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');

    // Respond to PING
    if (message == "PING") {
      Serial.println("PONG");

    // Handle LCD message
    } else if (message.startsWith("LCD ")) {
      lcdMessage = message.substring(4);
      Serial.println("LCD SUCCESS");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(lcdMessage);

    // Handle stepper motor command
    } else if (message.startsWith("MOVE ")) {
      // Example trajectory for testing
      int steps1[] = { 100, 200, -150, 300 };
      int steps2[] = { 200, -100, 250, -300 };
      int numSteps = sizeof(steps1) / sizeof(steps1[0]);

      for (int i = 0; i < numSteps; i++) {
        moveStepper(stepper1, steps1[i]);
        moveStepper(stepper2, steps2[i]);
      }

      // Update LCD with movement status
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Motors Moving");
      Serial.println("STEPPERS MOVED");

      
    }
  }
}
