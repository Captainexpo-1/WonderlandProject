int trigPin = 19;    // Trigger
int echoPin = 18;    // Echo
long duration, cm, inches;

#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "Happy Birthday Cara";
const char *password = "Happy Birthday";
static String server_path = "192.168.137.2:5000/theremin/";

void WiFiConnect() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(WiFi.status());
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void WiFiStationConnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Connected to AP successfully!");
}

void WiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void WiFiStationDisconnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Disconnected from WiFi access point");
  Serial.print("WiFi lost connection. Reason: ");
  Serial.println(info.wifi_sta_disconnected.reason);
  Serial.println("Trying to Reconnect");
  WiFiConnect();
}

void setup(){
  Serial.begin(115200);

  //Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // delete old config
  WiFi.disconnect(true);

  delay(1000);

  WiFi.onEvent(WiFiStationConnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_CONNECTED);
  WiFi.onEvent(WiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
  WiFi.onEvent(WiFiStationDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);

  WiFiConnect();
}

const int memory_len = 15;
int memory[memory_len];
int memory_i = 0;
int average = 0;
int outlier_limit = 50;

void loop(){
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
    // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
  
    // Read the signal from the sensor: a HIGH pulse whose
    // duration is the time (in microseconds) from the sending
    // of the ping to the reception of its echo off of an object.
    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH);
  
    // Convert the time into a distance
    cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
    memory[memory_i] = cm;
    int tmp = memory[memory_i], old_average = average;
    memory_i += 1;
    memory_i = memory_i % memory_len;

    average = ((average * (memory_len - 1)) - memory[memory_i] + tmp) * (memory_len - 1);
  
    if (abs(old_average - cm) >= outlier_limit) {
      Serial.print("OUTLIER:\nAVERAGE: ");
      Serial.println(old_average);
      Serial.print("DISTANCE: ");
      Serial.println(cm);
      Serial.println();
    } else {
      http.begin(server_path + cm);
      int httpResponseCode = http.GET();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      Serial.println();
      http.end();
    }
  }
}