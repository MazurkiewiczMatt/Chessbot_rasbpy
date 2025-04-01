#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;
bool ConnectedBollean = false;

// Sweep sequence: 30,180,35,180,40,180,45,180,50,180,55
const int angles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};
const int numAngles = sizeof(angles)/sizeof(angles[0]);
int currentAngle = 0;
unsigned long lastMove = 0;

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    myservo.attach(6);

    displayLCD("System Ready", "Connect to start");
    Serial.println("READY|Servo sequence system");
}

void loop() {
    if (!ConnectedBollean) {
        waitingDisplay();
    } else {
        handleSequence();
        checkSerial();
    }
}

void handleSequence() {
    if(millis() - lastMove >= 2000) { // 2 second interval
        // Update angle position
        currentAngle = (currentAngle + 1) % numAngles;

        // Move servo and update displays
        myservo.write(angles[currentAngle]);
        displayLCD("Position:", String(angles[currentAngle]) + " degrees");
        Serial.print("POS|");
        Serial.println(angles[currentAngle]);

        lastMove = millis();
    }
}

void checkSerial() {
    if(Serial.available() > 0) {
        String msg = Serial.readStringUntil('\n');
        msg.trim();

        if(msg.equalsIgnoreCase("PING")) {
            Serial.println("PONG");
            displayLCD("PING Received", "Active");
            delay(1000); // Brief LCD confirmation
        }
        else if(msg.startsWith("LCD")) {
            handleLCDCommand(msg.substring(3));
        }
    }
}

// Keep existing LCD functions unchanged
void displayLCD(String line1, String line2) { /* ... */ }
void handleLCDCommand(String lcdData) { /* ... */ }
void waitingDisplay() { /* ... */ }