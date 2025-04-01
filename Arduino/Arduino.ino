#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>
#include <Servo.h>

LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);
Servo myservo;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  myservo.attach(9);  // Changed to pin 9 for better PWM compatibility

  lcd.clear();
  lcd.print("Servo Test");
  lcd.setCursor(0, 1);
  lcd.print("Sweeping 30-150°");
}

void loop() {
  // Continuous sweep
  for(int pos = 30; pos <= 150; pos++) {
    updateServo(pos);
    checkSerial();
    delay(15);
  }
  for(int pos = 150; pos >= 30; pos--) {
    updateServo(pos);
    checkSerial();
    delay(15);
  }
}

void updateServo(int angle) {
  myservo.write(angle);
  delay(500);
  lcd.setCursor(0, 1);
  lcd.print("Angle: ");
  lcd.print(angle);
  lcd.print("°   "); // Clear residual characters
}

void checkSerial() {
  if(Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if(msg.equalsIgnoreCase("PING")) {
      Serial.println("PONG");
      lcd.clear();
      lcd.print("PING Received!");
      delay(100);
      lcd.clear();
      lcd.print("Servo Test");
    }
  }
}