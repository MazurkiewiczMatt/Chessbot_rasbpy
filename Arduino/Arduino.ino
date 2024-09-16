#include <Wire.h>
#include <LiquidCrystal_I2C_Hangul.h>

// Initialize the LCD with the I2C address (usually 0x27 or 0x3F)
LiquidCrystal_I2C_Hangul lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

String lcdMessage = "";  // Variable to store the text after LCD

void setup() {
  Wire.begin();
  Serial.begin(9600); // Begin serial communication
  Serial.println("Chessbot software initiated");
  Serial.println("Scanning for I2C devices...");


  Serial.print("Initializing LCD");
  lcd.init();
  lcd.backlight(); // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("INITIALIZED");
  Serial.print("Initialized LCD successfully");
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');

    if (message == "PING") {
      Serial.println("PONG");
    } else if (message.startsWith("LCD ")) {
      lcdMessage = message.substring(4);  // Save the text after "LCD " into lcdMessage
      Serial.print("LCD SUCCESS");
      lcd.clear(); // Clear the LCD
      lcd.setCursor(0, 0); // Set cursor to the top left
      lcd.print(lcdMessage); // Print the received data on the LCD
    }
  }
}
