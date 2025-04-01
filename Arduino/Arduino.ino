#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;
bool ConnectedBollean = false;

// Sweep pattern: 30, 180, 35, 180, 40... etc.
const int sweepAngles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};
const int numSteps = sizeof(sweepAngles) / sizeof(sweepAngles[0]);

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    myservo.attach(6);

    displayLCD("System Ready", "Send commands");
    Serial.println("STAT|System initialized");
}

void loop() {
    if (!ConnectedBollean) {
        waitingDisplay();
    } else {
        handleSerial();
    }
}

void handleSerial() {
    if (Serial.available() > 0) {
        String message = Serial.readStringUntil('\n');
        message.trim();

        if (message.equalsIgnoreCase("PING")) {
            Serial.println("PONG");
            displayLCD("PING Received", "System Active");
        }
        else if (message.equalsIgnoreCase("SWEEP")) {
            performServoSweep();
        }
        else if (message.startsWith("LCD")) {
            handleLCDCommand(message.substring(3));
        }
        else {
            Serial.println("ERR|Unknown command");
        }
    }
}

void performServoSweep() {
    Serial.println("STAT|Starting sweep pattern");
    displayLCD("Sweep Started", "Pattern running");

    for (int i = 0; i < numSteps; i++) {
        int target = sweepAngles[i];
        myservo.write(target);

        // LCD display
        String stepInfo = "Step " + String(i+1) + "/" + String(numSteps);
        String angleInfo = "Angle: " + String(target) + "°";
        displayLCD(stepInfo, angleInfo);

        // Serial feedback
        Serial.print("STAT|Position ");
        Serial.print(i+1);
        Serial.print("/");
        Serial.print(numSteps);
        Serial.print(": ");
        Serial.println(target);

        delay(2000);
    }

    displayLCD("Sweep Complete", "Cycle finished");
    Serial.println("DONE|Full pattern executed");
}

// Keep existing LCD functions
void displayLCD(String line1, String line2) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(line1);
    lcd.setCursor(0, 1);
    lcd.print(line2);
}

void handleLCDCommand(String lcdData) {
    int commaIndex = lcdData.indexOf(',');
    if (commaIndex != -1) {
        displayLCD(
            lcdData.substring(0, commaIndex).trim(),
            lcdData.substring(commaIndex+1).trim()
        );
        Serial.println("LCD|Update success");
    } else {
        Serial.println("ERR|LCD format: LCD line1,line2");
    }
}

void waitingDisplay() {
    static unsigned long lastChange = 0;
    static int msgIndex = 0;

    if (millis() - lastChange > 5000) {
        msgIndex = (msgIndex + 1) % numMessages;
        displayLCD(messages[msgIndex][0], messages[msgIndex][1]);
        lastChange = millis();
    }

    if (Serial.available()) {
        ConnectedBollean = true;
        displayLCD("Connected!", "Awaiting commands");
        delay(2000);
    }
}