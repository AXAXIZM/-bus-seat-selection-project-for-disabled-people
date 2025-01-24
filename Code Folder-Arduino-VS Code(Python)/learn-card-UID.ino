#include <SoftwareSerial.h>


#define RFID_TX_PIN 2 // RDM6300'ün TX pini Arduino'nun D2 pinine bağlıdık

SoftwareSerial rfidSerial(RFID_TX_PIN, -1); // RX pini kullanmıyoruz, bu yüzden -1

void setup() {
  Serial.begin(9600);          
  rfidSerial.begin(9600);     
  Serial.println("RDM6300 RFID Okuyucu Hazır!");
}
  
void loop() {
  if (rfidSerial.available()) { 
    byte data[14]; 
    int index = 0;

    while (rfidSerial.available() && index < 14) {
      data[index] = rfidSerial.read(); 
      index++;
      delay(5); 
    }

    if (index == 14) {
      
      if (data[0] == 0x02 && data[13] == 0x03) {
        Serial.print("Kart UID: ");
        for (int i = 1; i < 13; i++) {
          Serial.print((char)data[i]); // ASCII karakterlerini yazdır
          
        }
        delay(500);
        Serial.println();
      } else {
        Serial.println("Geçersiz veri!");
      }
    }
  }
}

//Serial Monitor Kısmında Yazan ID Kart UID'si olacak bunu diğer kod bloğunda kullanacağız