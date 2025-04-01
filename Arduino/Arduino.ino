#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

const int angles[] = {30, 180, 35, 180, 40, 180, 45, 180, 50, 180, 55};
const int emagPins[] = {14, 15};
int currentAngle = 0;

void setup() {
    lcd.init();
    lcd.backlight();
    myservo.attach(6);
    for(int pin : emagPins) pinMode(pin, OUTPUT);
}

void loop() {
    // Move down
    smoothMove(angles[currentAngle], 30);
    activateEmag(true);
    delay(4000);

    // Move up
    smoothMove(180, 30);
    activateEmag(false);

    currentAngle = (currentAngle + 1) % 5; // Only use first 5 down positions
}

void smoothMove(int target, int speed) {
    while(myservo.read() != target) {
        myservo.write(myservo.read() < target ? myservo.read()+1 : myservo.read()-1);
        lcd.clear();
        lcd.print("Position: ");
        lcd.print(myservo.read());
        delay(speed);
    }
}

void activateEmag(bool state) {
    for(int pin : emagPins) digitalWrite(pin, state);
    lcd.setCursor(0, 1);
    lcd.print(state ? "EMAG ON " : "EMAG OFF");
}