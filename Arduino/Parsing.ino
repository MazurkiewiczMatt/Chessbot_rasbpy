#include <Arduino.h>

//Commands: MOVE, LCD
//Delimiter: Comma (,)
//Termination: Newline (\n)
//MOVE Parameters: Two integers
//MOVE,<Integer1>,<Integer2>\n
//MOVE,150,250\n
//MOVE,-50,75\n
//LCD Parameters: Two strings
//LCD,<String1>,<String2>\n
//LCD,Hello Arduino,Serial Test\n
//LCD,Temp: 25C,Humidity: 60%\n
//Case Sensitivity: Commands must be in uppercase

// Function prototypes
void move(int a, int b);
void lcd(const String& line1, const String& line2);

// Buffer to store incoming messages
const uint16_t MAX_MESSAGE_LENGTH = 100;
char incomingMessage[MAX_MESSAGE_LENGTH];
uint16_t messageIndex = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready to receive commands.");
}

void loop() {
  // Read incoming serial data
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    
    // Debug: Print each received character
    Serial.print("Received Character: ");
    Serial.println(inChar);
    
    if (inChar == '\n') {
      incomingMessage[messageIndex] = '\0'; // Null-terminate the string
      
      // Debug: Print the complete received message
      Serial.print("Complete Message Received: ");
      Serial.println(incomingMessage);
      
      // Process the complete message
      processMessage(String(incomingMessage));
      
      messageIndex = 0; // Reset for next message
    }
    else {
      if (messageIndex < (MAX_MESSAGE_LENGTH - 1)) {
        incomingMessage[messageIndex++] = inChar;
      }
      else {
        // Buffer overflow, reset
        Serial.println("Error: Message too long.");
        messageIndex = 0;
      }
    }
  }
}

void processMessage(String msg) {
  msg.trim(); // Remove leading/trailing whitespace
  
  // Debug: Print the trimmed message
  Serial.print("Processing Message: ");
  Serial.println(msg);
  
  if (msg.startsWith("MOVE")) {
    // Expected format: MOVE,number1,number2
    int firstComma = msg.indexOf(',');
    
    // Debug: Print position of first comma
    Serial.print("MOVE Command - First Comma Position: ");
    Serial.println(firstComma);
    
    if (firstComma == -1) {
      Serial.println("Error: Invalid MOVE format. Missing commas.");
      return;
    }
    
    int secondComma = msg.indexOf(',', firstComma + 1);
    
    // Debug: Print position of second comma
    Serial.print("MOVE Command - Second Comma Position: ");
    Serial.println(secondComma);
    
    if (secondComma == -1) {
      Serial.println("Error: MOVE requires two integers separated by a comma.");
      return;
    }
    
    String num1Str = msg.substring(firstComma + 1, secondComma);
    String num2Str = msg.substring(secondComma + 1);
    
    // Debug: Print extracted number strings
    Serial.print("MOVE Command - Number 1 String: ");
    Serial.println(num1Str);
    Serial.print("MOVE Command - Number 2 String: ");
    Serial.println(num2Str);
    
    int num1 = num1Str.toInt();
    int num2 = num2Str.toInt();
    
    // Debug: Print converted integer values
    Serial.print("MOVE Command - Parsed Integer 1: ");
    Serial.println(num1);
    Serial.print("MOVE Command - Parsed Integer 2: ");
    Serial.println(num2);
    
    // Call the move function
    move(num1, num2);
    
  }
  else if (msg.startsWith("LCD")) {
    // Expected format: LCD,Line1,Line2
    int firstComma = msg.indexOf(',');
    
    // Debug: Print position of first comma
    Serial.print("LCD Command - First Comma Position: ");
    Serial.println(firstComma);
    
    if (firstComma == -1) {
      Serial.println("Error: Invalid LCD format. Missing commas.");
      return;
    }
    
    int secondComma = msg.indexOf(',', firstComma + 1);
    
    // Debug: Print position of second comma
    Serial.print("LCD Command - Second Comma Position: ");
    Serial.println(secondComma);
    
    if (secondComma == -1) {
      Serial.println("Error: LCD requires two strings separated by a comma.");
      return;
    }
    
    String line1 = msg.substring(firstComma + 1, secondComma);
    String line2 = msg.substring(secondComma + 1);
    
    // Debug: Print extracted line strings
    Serial.print("LCD Command - Line 1: ");
    Serial.println(line1);
    Serial.print("LCD Command - Line 2: ");
    Serial.println(line2);
    
    // Call the lcd function
    lcd(line1, line2);
    
  }
  else {
    Serial.println("Error: Unknown command.");
  }
}

void move(int a, int b) {
  // Debug: Before processing move
  Serial.println("Executing move() function...");
  Serial.print("move() - Parameter a: ");
  Serial.println(a);
  Serial.print("move() - Parameter b: ");
  Serial.println(b);
  
  // TODO: Implement your movement logic here
  
  // Debug: After processing move
  Serial.println("move() function execution completed.");
}

void lcd(const String& line1, const String& line2) {
  // Debug: Before processing lcd
  Serial.println("Executing lcd() function...");
  Serial.print("lcd() - Line 1: ");
  Serial.println(line1);
  Serial.print("lcd() - Line 2: ");
  Serial.println(line2);
  
  // TODO: Implement your LCD display logic here
  
  // Debug: After processing lcd
  Serial.println("lcd() function execution completed.");
}
