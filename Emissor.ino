#include <RH_ASK.h>
#include <SPI.h> // Necessário mesmo que não use SPI diretamente

RH_ASK driver(2000, 5, 4, 0);

void setup() {
    driver.init();
    Serial.begin(115200);
    Serial.println("Fechadura controlada por voz");
}

void loop() {

    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
       
        driver.send((uint8_t*)command.c_str(), command.length());
        driver.waitPacketSent();
        Serial.println("Comando enviado: " + command);
        
    }
}
