#include <RH_ASK.h>
#include <SPI.h>

RH_ASK driver(2000, 4, 5, 0);

// Pinos para LEDs
const int ledAberto = 12;   // LED D6 - Estado aberto
const int ledFechado = 13;  // LED D7 - Estado fechado

// Estados da fechadura
enum EstadoFechadura {
    ABERTO,
    FECHADO
};
EstadoFechadura estadoAtual = FECHADO;  // Inicialmente a fechadura está fechada

// Frases chave para comparação
String chaveAbrir = "abrir por favor";
String chaveFechar = "fechar a porta";

void setup() {
    driver.init();
    Serial.begin(115200);

    pinMode(ledAberto, OUTPUT);
    pinMode(ledFechado, OUTPUT);

    Serial.println("Fechadura iniciada. A aguardar comandos...");
    atualizarLEDs();
}

void loop() {
    uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
    uint8_t buflen = sizeof(buf);

    if (driver.recv(buf, &buflen)) {  // Mensagem recebida
        buf[buflen] = '\0';  // Garantir que seja uma string válida
        String command = String((char*)buf);

        // Comparar comando recebido com as chaves
        if (command.equals(chaveAbrir)) {
            if (estadoAtual == FECHADO) {
                estadoAtual = ABERTO;
                Serial.println("Fechadura aberta.");
            }
        } else if (command.equals(chaveFechar)) {
            if (estadoAtual == ABERTO) {
                estadoAtual = FECHADO;
                Serial.println("Fechadura fechada.");
            }
        } else {
            Serial.println("Comando desconhecido: " + command);
        }
        atualizarLEDs();
    }
}

// Função para atualizar os LEDs com base no estado atual
void atualizarLEDs() {
    switch (estadoAtual) {
        case FECHADO:
            digitalWrite(ledFechado, HIGH);  // LED aceso quando fechado
            digitalWrite(ledAberto, LOW);    // LED apagado quando fechado
            break;

        case ABERTO:
            digitalWrite(ledFechado, LOW);   // LED apagado quando aberto
            digitalWrite(ledAberto, HIGH);   // LED aceso quando aberto
            break;
    }
}