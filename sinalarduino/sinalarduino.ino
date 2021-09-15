
//esteira deve ser ligada na porta 5 / LED_BUILTIN
int esteira = 7; 
int sinal2 = 9; //Saida do sinal a cada 3 minutos         

long tempoanterior = 0;
long tempo = 1800; //3 minutos

void setup() { 
  pinMode(esteira, OUTPUT);
  pinMode(sinal2, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if(millis() >= tempoanterior+20000){
    tempoanterior = millis();
    digitalWrite(sinal2, HIGH);
    tempoanterior = millis();
    
  }else if(millis() > tempoanterior + 3000){ 
    digitalWrite(sinal2, LOW);
  }
  
  while(Serial.available()){
    char situacao = Serial.read();

    if(situacao == '0'){
    digitalWrite(esteira, LOW);
    // wait for 3 seconds to see the dimming effect
    delay(100);
    }

    if(situacao == '5'){
    digitalWrite(esteira, HIGH);
    delay(100);
    }
  }
}
