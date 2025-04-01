#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

const int angles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};

void setup() {
    lcd.init();
    lcd.backlight();
    myservo.attach(6);
}

void loop() {
    for(int i = 0; i < sizeof(angles)/sizeof(angles[0]); i++) {
        myservo.write(angles[i]);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Position:");
        lcd.setCursor(0, 1);
        lcd.print(angles[i]);
        lcd.print(" degrees");
        delay(2000);
    }
}