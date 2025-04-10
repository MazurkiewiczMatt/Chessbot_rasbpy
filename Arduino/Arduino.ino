#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

// Initialize the LCD at I2C address 0x27 with 16 columns and 2 rows
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2);

void setup() {
  // Initialize I2C communication
  Wire.begin();

  // Initialize the LCD
  lcd.init();
  // Turn on the LCD backlight
  lcd.backlight();

  // Clear the display and set the cursor to the beginning of the first line
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Hello, World!");

  // Set the cursor to the beginning of the second line and print another message
  lcd.setCursor(0, 1);
  lcd.print("LCD Test");
}

void loop() {
  // Nothing to do here
}
