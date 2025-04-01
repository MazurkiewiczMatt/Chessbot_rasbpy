#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // Address 0x27, 16x2
Servo myservo;
bool ConnectedBollean = 0;

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    myservo.attach(6);  // Servo on pin 6

    lcd.clear();
    lcd.print("System Ready");
    lcd.setCursor(0, 1);
    lcd.print("Send commands");
    Serial.println("READY|Servo test system initialized");
}

void loop() {
    if (ConnectedBollean == 0) {
        waitingDisplay();
    } else {
        if (Serial.available() > 0) {
            String message = Serial.readStringUntil('\n');
            message.trim();

            if (message.equalsIgnoreCase("PING")) {
                Serial.println("PONG");
                displayLCD("PONG Received", "System Ready");
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
}

void performServoSweep() {
    for(int i = 0; i < 5; i++) {
        myservo.write(50);
        displayLCD("Sweep " + String(i+1), "Position: 50°");
        Serial.println("STAT|Moving to 50°");
        delay(1000);

        myservo.write(180);
        displayLCD("Sweep " + String(i+1), "Position: 180°");
        Serial.println("STAT|Moving to 180°");
        delay(1000);
    }
    displayLCD("Sweep Complete", "5 cycles done");
    Serial.println("DONE|Sweep completed");
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
        String line1 = lcdData.substring(0, commaIndex);
        line1.trim();
        String line2 = lcdData.substring(commaIndex + 1);
        line2.trim();
        displayLCD(line1, line2);
        Serial.println("LCD|Update success");
    } else {
        Serial.println("ERR|LCD format: LCD line1,line2");
    }
}

void waitingDisplay() {
    static unsigned long lastUpdate = 0;
    static int msgIndex = 0;

    if(millis() - lastUpdate > 5000) {
        msgIndex = random(numMessages);
        displayLCD(messages[msgIndex][0], messages[msgIndex][1]);
        lastUpdate = millis();
    }

    if(Serial.available()) {
        ConnectedBollean = true;
        displayLCD("Connected!", "Awaiting commands");
        delay(2000);
    }
}