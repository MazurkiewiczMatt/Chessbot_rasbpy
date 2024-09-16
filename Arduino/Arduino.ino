#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Initialize the LCD with the I2C address (usually 0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

String lcdMessage = "";  // Variable to store the text after "LCD"

void setup() {
  lcd.init(); // Initialize the LCD
  lcd.backlight(); // Turn on the backlight
  Serial.begin(9600); // Begin serial communication
  Serial.println("Chessbot software initiated");
  Serial.setTimeout(20); // Set the timeout for serial reading
  lcd.setCursor(0, 0);
  lcd.print("Waiting for data");
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n'); // Read the serial data

    if (message == "PING") {
      Serial.println("PONG");
    } else if (message.startsWith("LCD ")) {
      lcdMessage = message.substring(4);  // Extract the text after "LCD"
      lcd.clear(); // Clear the LCD
      lcd.setCursor(0, 0); // Set cursor to the top left
      lcd.print(lcdMessage); // Display the message on the LCD
      Serial.print("LCD SUCCESS");
      Serial.println(lcdMessage);  // Echo back the message
    }
  }
}
