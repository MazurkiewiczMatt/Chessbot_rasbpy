#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

const int angles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};
int currentTarget = 0;
int currentPos = 30;
unsigned long lastMove = 0;
const int moveInterval = 30; // Time between small steps (ms)

void setup() {
    lcd.init();
    lcd.backlight();
    myservo.attach(6);
    myservo.write(currentPos);
    updateDisplay();
}

void loop() {
    if(millis() - lastMove >= moveInterval) {
        // Calculate movement step (3x slower by using smaller steps)
        int target = angles[currentTarget];
        int step = (target > currentPos) ? 1 : -1;

        currentPos += step;
        myservo.write(currentPos);

        // Update display only when reaching target
        if(currentPos == target) {
            currentTarget = (currentTarget + 1) % (sizeof(angles)/sizeof(angles[0]));
            updateDisplay();
        }

        lastMove = millis();
    }
}

void updateDisplay() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Moving to:");
    lcd.setCursor(0, 1);
    lcd.print(angles[currentTarget]);
    lcd.print(" degrees");
}