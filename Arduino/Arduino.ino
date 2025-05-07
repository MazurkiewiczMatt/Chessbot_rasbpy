#include <AccelStepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>
//good
#define motorInterfaceType AccelStepper::DRIVER
//good
AccelStepper stepper1(motorInterfaceType, 3, 2);
AccelStepper stepper2(motorInterfaceType, 5, 4);
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;
//good
bool ConnectedBollean = 0;
const int homeButton1Pin = 7;
const int homeButton2Pin = 8;
//good
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
const unsigned long debounceDelay = 50;
const int homingSteps = 1230;
//^^ to review homing
int MaxSpeed = 200;
int MaxAcc = 120;

const int emagPins[] = {14, 15};
//good
int currentPos = 30;
const int moveInterval = 30;
//^^to review homing

const char* messages[][2] = {
  {"1234567890123456", "1234567890123456"},
  {"revving chess", "engine"},
  {"inferring piece", "locations"},
  {"plotting", "check mate"},
  {"rubbing one off", "to clear head"},
  {"innovating", "strategy"},
  {"predicting your", "every possible move"},
  {"praying to", "deepBlue"},
  {"Effecting", "Oberth"},
  {"Cleaning", "transfer windows"},
  {"Electro-", "liminescing"},
  {"Defending", "king"},
  {"Multiplexing", "read switches"},
  {"Boxing", "gears"},
  {"Venting", "heat"},
  {"Consulting", "Stockfish"},
  {"Electrifying", "fields"},
  {"Recursive", "selfplay"},
  {"Optimizing", "Estimator"},
  {"Machine", "Learning"},
  {"Beating Korean", "Grandmaster"},
  {"Sparring", "Kasparov"},
  {"Arguing with", "Fide"},
  {"Qualifying", "to candidates"},
  {"Forgetting", "Board layout"},
  {"Watching", "Chess gambit"},
  {"Confusing", "pawn captures"},
  {"Randomly", "promoting"},
  {"Adjusting", "Neurons"},
  {"Studying Bong", "Cloud opening"},
  {"Hating", "London"},
  {"Waiting for", "Another input"},
  {"take take take", "take and take"},
  {"Capturing", "Juicers"},
  {"Forking", "knights"},
  {"sacrificing the", "ROOK"},
  {"Another", "interesting text"},
  {"Something with", "times new Roman"},
  {"Destroying", "hotel room"},
  {"Communication", "with yogurt"},
  {"Glasses to", "throw opponent off"},
  {"<><><><>", "><><><><"},
  {"Failing", "Compiling (JOKE)"},
  {"Almost last", "message"},
  {"01100010", "10011100"},
  {"Defending", "outcome"}
};
const int numMessages = sizeof(messages) / sizeof(messages[0]);
//good
void displayLCD(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}
//good

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
//good
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
//good
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
  if ((step1Value.length() == 0) || (step2Value.length() == 0)) {
    Serial.println("Invalid step values. Ensure both step1 and step2 are integers.");
    return;
  }
  moveSteppers(step1, step2);
  displayLCD("Motors Moving", "Step1: " + String(step1) + " Step2: " + String(step2));
}
//good
void performHoming(AccelStepper& stepper, bool initialDirectionPositive, int buttonPin, String stepperName) {
  // Configure reduced speed and acceleration
  int originalSpeed = MaxSpeed;
  int originalAcc = MaxAcc;
  stepper.setMaxSpeed(originalSpeed / 2);
  stepper.setAcceleration(originalAcc / 2);

  // Determine homing direction
  int initialMoveDir = initialDirectionPositive ? 2200 : -2200;
  int retreatMoveDir = initialDirectionPositive ? -homingSteps : homingSteps;

  displayLCD("Homing " + stepperName, initialMoveDir < 0 ? "Moving Negative" : "Moving Positive");
  stepper.move(initialMoveDir);

  unsigned long* lastDebounce = (stepperName == "Stepper1") ? &lastDebounceTime1 : &lastDebounceTime2;

  while (stepper.distanceToGo() != 0) {
    stepper.run();
    if (digitalRead(buttonPin) == LOW) {
      unsigned long currentTime = millis();
      if (currentTime - *lastDebounce > debounceDelay) {
        *lastDebounce = currentTime;
        stepper.stop();
        displayLCD("Homing " + stepperName, "Stopping...");
        break;
      }
    }
  }

  displayLCD("Homing " + stepperName, "Moving back...");
  stepper.move(retreatMoveDir);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }

  stepper.setCurrentPosition(0);

  // Restore full speed and acceleration
  stepper.setMaxSpeed(originalSpeed);
  stepper.setAcceleration(originalAcc);

  displayLCD(stepperName + " Homed", "");
}

//^^to review homing
void homeAllSteppers() {
  displayLCD("Homing Initiated", "");
  // Stepper1 moves negative using homeButton2Pin
  performHoming(stepper1, false, homeButton2Pin, "Stepper1");
  // Stepper2 moves positive using homeButton1Pin
  performHoming(stepper2, true, homeButton1Pin, "Stepper2");
  displayLCD("Homing Complete", "");
}
//^^to review homing
void Manuver() {


  stepper1.setMaxSpeed(MaxSpeed*3);
  stepper1.setAcceleration(MaxAcc*5);
  stepper2.setMaxSpeed(MaxSpeed*3);
  stepper2.setAcceleration(MaxAcc*5);
  moveSteppers(250,-250);
  moveSteppers(-100,100);
  stepper1.setMaxSpeed(MaxSpeed);
  stepper1.setAcceleration(MaxAcc);
  stepper2.setMaxSpeed(MaxSpeed);
  stepper2.setAcceleration(MaxAcc);


    Serial.println("MANUVER DONE");

}
void waitingDisplay() {
  static unsigned long startTime = millis();
  static unsigned long lastMessageTime = 0;
  static int messageIndex = random(numMessages);
  const unsigned long timeout = 90000;
  if (millis() - startTime >= timeout) {
    displayLCD("90s Mark:", "Raspberry Not Connected");
    startTime = millis();
    return;
  }
  if (millis() - lastMessageTime >= 5000) {
    messageIndex = random(numMessages);
    displayLCD(messages[messageIndex][0], messages[messageIndex][1]);
    lastMessageTime = millis();
  }
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();
    if (message.length() > 0) {
      ConnectedBollean = 1;
    }
  }
}
//good
void handleElectromagnetDrop(String cmdData) {
  cmdData.trim();
  int targetAngle = cmdData.toInt();
  int step = (targetAngle > currentPos) ? 1 : -1;
  while (currentPos != targetAngle) {
    currentPos += step;
    myservo.write(currentPos);
    delay(moveInterval);
  }
  digitalWrite(emagPins[0], HIGH);
  digitalWrite(emagPins[1], HIGH);
  Serial.println("EM_dropped");
}
//good
void handleElectromagnetRaise(String cmdData) {
  cmdData.trim();
  int targetAngle = cmdData.toInt();
  int step = (targetAngle > currentPos) ? 1 : -1;
  while (currentPos != targetAngle) {
    currentPos += step;
    myservo.write(currentPos);
    delay(moveInterval);
  }
  digitalWrite(emagPins[0], LOW);
  digitalWrite(emagPins[1], LOW);
  Serial.println("EM_rose");
}
//good
void handleElectromagnetTurn(String command) {
  if (command.equalsIgnoreCase("EM_ON")) {
    digitalWrite(emagPins[0], HIGH);
    digitalWrite(emagPins[1], HIGH);
    Serial.println("EM_on");
  } else if (command.equalsIgnoreCase("EM_OFF")) {
    digitalWrite(emagPins[0], LOW);
    digitalWrite(emagPins[1], LOW);
    Serial.println("EM_off");
  }
}
//good
void setup() {
  pinMode(homeButton1Pin, INPUT_PULLUP);
  pinMode(homeButton2Pin, INPUT_PULLUP);
  for (int i = 0; i < 2; i++) {
    pinMode(emagPins[i], OUTPUT);
    digitalWrite(emagPins[i], LOW);
  }
  Wire.begin();
  Serial.begin(9600);
  Serial.setTimeout(100);
  Serial.println("Chessbot software initiated");
  lcd.init();
  lcd.backlight();
  stepper1.setMaxSpeed(MaxSpeed);
  stepper1.setAcceleration(MaxAcc);
  stepper2.setMaxSpeed(MaxSpeed);
  stepper2.setAcceleration(MaxAcc);
  myservo.attach(6);
  myservo.write(currentPos);
}


void loop() {
  if (!ConnectedBollean) {
    waitingDisplay();
  } else {
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
      } else if (message.equalsIgnoreCase("MANUVER")) {
        Manuver();
      } else if (message.startsWith("EM_D")) {
        handleElectromagnetDrop(message.substring(4));
      } else if (message.startsWith("EM_R")) {
        handleElectromagnetRaise(message.substring(4));
      } else if (message.startsWith("EM_ON") || message.startsWith("EM_OFF")) {
        handleElectromagnetTurn(message);
      } else {
        Serial.println("Unknown command");
      }
    }
  }
}