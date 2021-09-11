//esteira deve ser ligada na porta 5 / LED_BUILTIN
int esteira = 5; 
int sinal2 = 3; //Saida do sinal a cada 3 minutos         

long tempoanterior = 0;
long tempo = 180000; //3 minutos

void setup() { 
  pinMode(esteira, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if(millis() >= tempoanterior+180000){
    tempoanterior = millis();
    digitalWrite(sinal2, HIGH);
    delay(3000);
    digitalWrite(sinal2, LOW);
  }
  
  while(Serial.available()){
    char situacao = Serial.read();

    if(situacao == '0'){
    digitalWrite(esteira, HIGH);
    // wait for 3 seconds to see the dimming effect
    delay(1000);
    }

    if(situacao == '5'){
    digitalWrite(esteira, LOW);
    delay(1000);
    }
  }
}
