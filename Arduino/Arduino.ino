void setup() {
  Serial.begin(9600);
  Serial.println("Chessbot software initiated");
  Serial.setTimeout(50);
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    if (message == "PING") {
      Serial.println("PONG");
    }
  }
}