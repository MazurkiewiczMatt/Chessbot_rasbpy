#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // I2C address 0x27
Servo myservo;

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    myservo.attach(6);  // Servo on pin 6

    // Initial display
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Servo Test Ready");
    lcd.setCursor(0, 1);
    lcd.print("Send 0-180 deg");
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.toInt() >= 0 && input.toInt() <= 180) {
            int angle = input.toInt();

            // Update LCD
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Moving to:");
            lcd.setCursor(0, 1);
            lcd.print(String(angle) + " degrees");

            // Move servo
            myservo.write(angle);
            Serial.print("Moved to: ");
            Serial.println(angle);
        }
        else {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Invalid input!");
            lcd.setCursor(0, 1);
            lcd.print("Use 0-180");
            Serial.println("Error: Invalid angle");
        }
    }
}