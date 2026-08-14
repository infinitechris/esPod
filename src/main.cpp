#include <Arduino.h>
#include <M5Cardputer.h>

void printStatus(const char *msg) {
  Serial.println(msg);
  M5.Lcd.fillScreen(TFT_BLACK);
  M5.Lcd.setTextColor(TFT_WHITE);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.println(msg);
}

void setup() {
  Serial.begin(115200);
  M5.begin();

  M5.Lcd.setBrightness(80);
  M5.Lcd.fillScreen(TFT_BLACK);
  M5.Lcd.setTextColor(TFT_GREEN);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.println("Cardputer ADV boot OK");
  M5.Lcd.println("Waiting for tests...");

  Serial.println("Cardputer ADV boot OK");
  Serial.println("Ready for bring-up tests.");
}

void loop() {
  M5.update();

  if (M5.BtnA.wasPressed()) {
    printStatus("BtnA pressed");
  }

  if (M5.BtnB.wasPressed()) {
    printStatus("BtnB pressed");
  }

  if (M5.BtnC.wasPressed()) {
    printStatus("BtnC pressed");
  }

  delay(50);
}
