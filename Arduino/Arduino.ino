this is electromagnet and servo functionalities:
#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

const int angles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};
const int emagPins[] = {14, 15};
int currentTarget = 0;
int currentPos = 30;
unsigned long lastMove = 0;
const int moveInterval = 30;
bool waiting = false;
unsigned long waitStart = 0;

void setup() {
    lcd.init();
    lcd.backlight();
    myservo.attach(6);
    for(int pin : emagPins) pinMode(pin, OUTPUT);
    updateDisplay();
}

void loop() {
    if(waiting) {
        if(millis() - waitStart >= 4000) {
            waiting = false;
            currentTarget = (currentTarget + 1) % (sizeof(angles)/sizeof(angles[0]));
            digitalWrite(emagPins[0], LOW);
            digitalWrite(emagPins[1], LOW);
            updateDisplay();
        }
        return;
    }

    if(millis() - lastMove >= moveInterval) {
        int target = angles[currentTarget];
        int step = (target > currentPos) ? 1 : -1;

        currentPos += step;
        myservo.write(currentPos);

        if(currentPos == target) {
            if(target != 180) { // Down position
                digitalWrite(emagPins[0], HIGH);
                digitalWrite(emagPins[1], HIGH);
                waiting = true;
                waitStart = millis();
                lcd.clear();
                lcd.print("HOLDING AT:");
                lcd.setCursor(0, 1);
                lcd.print(target);
                lcd.print("°  EMAG ON");
            }
            else {
                currentTarget = (currentTarget + 1) % (sizeof(angles)/sizeof(angles[0]));
                updateDisplay();
            }
        }
        lastMove = millis();
    }
}

void updateDisplay() {
    lcd.clear();
    lcd.print("Moving to:");
    lcd.setCursor(0, 1);
    lcd.print(angles[currentTarget]);
    lcd.print("°");
}