#include <SoftwareSerial.h>

#define RFID_TX_PIN 2 // RDM6300'ün TX pini Arduino'nun D2 pinine bağlı
SoftwareSerial rfidSerial(RFID_TX_PIN, -1); // RX pini kullanılmayacak

String authorizedUID = "BURAYA GELECEK KART UID"; // Yetkili kart UID'si bu kızma yzlr bunu öğrenmek için başka bir dosya lazım onu da aktaracağım
bool cardRead = false;  // Kartın okunduğu durumu takip etmek için bir değişken

void setup() {
  Serial.begin(9600);          
  rfidSerial.begin(9600);      
  Serial.println("RDM6300 RFID Okuyucu Hazır!");
}

void loop() {
  if (rfidSerial.available() && !cardRead) { // Eğer RFID verisi varsa ve kart daha önce okunmadıysa
    byte data[14]; // RFID modülü her okuma için 14 byte veri gönderir
    int index = 0;

    while (rfidSerial.available() && index < 14) {
      data[index] = rfidSerial.read(); // Gelen veriyi oku
      index++;
      delay(5); // Veri tam alınması için küçk bir gecikme
    }

    if (index == 14) {
      // Veri doğruluğunu kontrol etmek içcin (başlangıç ve bitiş baytları)
      if (data[0] == 0x02 && data[13] == 0x03) {
        String uid = "";
        for (int i = 1; i < 13; i++) {
          uid += (char)data[i]; // UID'yi al ve string'e dönüştür
        }
        Serial.println(uid); // Okunan UID'yi seri port üzerinden gönder
        cardRead = true; // Kart okundu, tekrar okunmasın
        delay(500); // 
      } else {
        Serial.println("Geçersiz veri!");
      }
    }
  }

  // Kart okuduktan sonra belli bir süre sonra tekrar okuma yapılabilmesi için bekleme
  if (cardRead) {
    delay(5000);  // Kart okuduktan sonra 5 saniye bekle
    cardRead = false;  // Okuma işlemi bitiyor, kart tekrar okunabilir
  }
}
