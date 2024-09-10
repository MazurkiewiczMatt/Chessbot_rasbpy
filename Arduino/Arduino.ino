void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\\n');
    if (message == "PING") {
      Serial.println("PONG");
    }
  }
}