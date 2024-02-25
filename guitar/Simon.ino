void setup(){
    Serial.begin(9600);
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT_PULLUP);
    pinMode(5, INPUT_PULLUP);
    pinMode(6, INPUT_PULLUP);
    pinMode(7, INPUT_PULLUP);
}
void loop(){
    int a = digitalRead(3) ^ 1;
    int b = digitalRead(4) ^ 1;
    int c = digitalRead(5) ^ 1;
    int d = digitalRead(6) ^ 1;
    Serial.println(String(a) + " " + String(b) + " " + String(c) + " " + String(d));
}