#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "Pain";
const char *password = "12345678";
static String server_path = "192.168.137.1:5000/drums/";

const int cymbal = 16, mainDrum = 2, leftDrum = 4, rightDrum = 15;

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

  // delete old config
  WiFi.disconnect(true);

  delay(1000);

  WiFi.onEvent(WiFiStationConnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_CONNECTED);
  WiFi.onEvent(WiFiGotIP, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_GOT_IP);
  WiFi.onEvent(WiFiStationDisconnected, WiFiEvent_t::ARDUINO_EVENT_WIFI_STA_DISCONNECTED);

  WiFiConnect();
}

bool mainDrumOn = false;
bool cymbalOn = false;
bool leftDrumOn = false;
bool rightDrumOn = false;

int mainDrumRead, cymbalRead, leftDrumRead, rightDrumRead;

void loop(){
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    mainDrumRead = digitalRead(mainDrum);
    cymbalRead = digitalRead(cymbal);
    leftDrumRead = digitalRead(leftDrum);
    rightDrumRead = digitalRead(rightDrum);
    if (!mainDrumOn && mainDrumRead) {
      http.begin(server_path + "bass");
      int httpResponseCode = http.GET();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      http.end();
      mainDrumOn = true;
    } else if (mainDrumOn && !mainDrumRead) {
      mainDrumOn = false;
    }
    if (!cymbalOn && cymbalRead) {
      http.begin(server_path + "crash");
      int httpResponseCode = http.GET();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      http.end();
      cymbalOn = true;
    } else if (cymbalOn && !cymbalRead) {
      cymbalOn = false;
    }
    if (!leftDrumOn && leftDrumRead) {
      http.begin(server_path + "snare");
      int httpResponseCode = http.GET();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      http.end();
      leftDrumOn = true;
    } else if (leftDrumOn && !leftDrumRead) {
      leftDrumOn = false;
    }
    if (!rightDrumOn && rightDrumRead) {
      http.begin(server_path + "tom");
      int httpResponseCode = http.GET();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      http.end();
      rightDrumOn = true;
    } else if (rightDrumOn && !rightDrumRead) {
      rightDrumOn = false;
    }
  }
}
