#include <Arduino.h>
int step1 = 15;
int dir1  = 2;
int step2 = 4;
int dir2  = 5;
int step3 = 18;
int dir3 = 19;
int MS1_dc1_3 = 26;
int MS2_dc1_3 = 25;
int MS3_dc1_3 = 33;
int MS1_dc2 = 12;
int MS2_dc2 = 14;
int MS3_dc2 = 27;
int ena = 23;
#define limitx 32
#define limity 35
#define limitz 34
int CB1;
int CB2;
int CB3;
int sethome;
void setup() {
  Serial.begin(115200);
  pinMode(step1, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(step2,OUTPUT);
  pinMode(dir2,OUTPUT);
  pinMode(step3,OUTPUT);
  pinMode(dir3, OUTPUT);
  pinMode(ena, OUTPUT);
  pinMode(MS1_dc1_3, OUTPUT);
  pinMode(MS2_dc1_3, OUTPUT);
  pinMode(MS3_dc1_3, OUTPUT);
  pinMode(MS1_dc2, OUTPUT);
  pinMode(MS2_dc2, OUTPUT);
  pinMode(MS3_dc2, OUTPUT);
  pinMode(limitx , INPUT);
  pinMode(limity , INPUT);
  pinMode(limitz , INPUT);
  // A4988: 1/16 microstep
  digitalWrite(MS1_dc1_3, HIGH);
  digitalWrite(MS2_dc1_3, HIGH);
  digitalWrite(MS3_dc1_3, HIGH);
  digitalWrite(MS1_dc2, LOW);
  digitalWrite(MS2_dc2, LOW);
  digitalWrite(MS3_dc2, LOW);

  // Luôn enable driver
  digitalWrite(ena, LOW);
}

void quay90_dc1(bool chieu) {
  digitalWrite(dir1, chieu);

  delayMicroseconds(100); // cho DIR ổn định

  for (int i = 0; i < 3000; i++) {
    digitalWrite(step1, HIGH);
    delayMicroseconds(1000);
    digitalWrite(step1, LOW);
    delayMicroseconds(1000);
  }
}

void quay90_dc3(bool chieu) {
  digitalWrite(dir3, chieu);

  delayMicroseconds(100); // cho DIR ổn định

  for (int i = 0; i < 3000; i++) {
    digitalWrite(step3, HIGH);
    delayMicroseconds(1000);
    digitalWrite(step3, LOW);
    delayMicroseconds(1000);

  }
}
void quay90_dc2(bool chieu) {
  digitalWrite(dir2, chieu);

  delayMicroseconds(100); // cho DIR ổn định

  for (int i = 0; i < 188; i++) {
    digitalWrite(step2, HIGH);
    delay(18);
    digitalWrite(step2, LOW);
    delay(18);
  }
}
void Sethome(){
  digitalWrite(ena,LOW);
  delayMicroseconds(10);
  digitalWrite(dir2, LOW);
  for(int i =0 ; i<188; i++){
    CB2 = digitalRead(limity);
    if(CB2 == 1){
      break;
    }
    digitalWrite(step2,HIGH);
    delay(18);
    digitalWrite(step2,LOW);
    delay(18);

  }
  digitalWrite(dir2, HIGH);
  for(int i = 0 ; i<376; i++){
    CB2 = digitalRead(limity);
    if(CB2 == 1){
      break;
    }
    digitalWrite(step2,HIGH);
    delay(18);
    digitalWrite(step2,LOW);
    delay(18);

  }
  digitalWrite(dir3, HIGH);
  for(int i = 0; i< 3000; i++){
    CB3 = digitalRead(limitz);
    if(CB3 == 1){
      break;
    }
    digitalWrite(step3,HIGH);
    delayMicroseconds(1000);
    digitalWrite(step3,LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(dir3, LOW);
  for(int i = 0; i< 6000; i++){
    CB3 = digitalRead(limitz);
    if(CB3 == 1){
      break;
    }
    digitalWrite(step3,HIGH);
    delayMicroseconds(1000);
    digitalWrite(step3,LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(dir1,HIGH);
  for(int i = 0; i< 3000; i++){
    CB1 = digitalRead(limitx);
    if(CB1 == 1){
      break;
    }
    digitalWrite(step1,HIGH);
    delayMicroseconds(1000);
    digitalWrite(step1,LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(dir1,LOW);
  for(int i = 0; i< 6000; i++){
    CB1 = digitalRead(limitx);
    if(CB1 == 1){
      break;
    }
    digitalWrite(step1,HIGH);
    delayMicroseconds(1000);
    digitalWrite(step1,LOW);
    delayMicroseconds(1000);
  }
}
void loop() {
  while(Serial.available()){
    String data = Serial.readString();
    delayMicroseconds(5);
    if(data[0] == 'Q' ){
      Serial.println("quay 90 do theo chieu nghich");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc1(HIGH);
    }
    else if (data[0] == 'W'){
      Serial.println("quay 90 do theo chieu thuan");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc1(LOW);
    }
    else if(data[0] == 'E' ){
      Serial.println("quay 90 do theo chieu THUAN");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc2(LOW);
    }
    else if (data[0] == 'R'){
      Serial.println("quay 90 do theo chieu NGHICH");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc2(HIGH);
    }
    else if(data[0] == 'T' ){
      Serial.println("quay 90 do theo chieu nghich");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc3(HIGH);
    }
    else if (data[0] == 'Y'){
      Serial.println("quay 90 do theo chieu thuan");
      digitalWrite(ena,LOW);
      delayMicroseconds(5);
      quay90_dc3(LOW);
    }
    else if (data[0] == 'O') {
      Serial.println("Tat dong co");
      digitalWrite(ena,HIGH);
    }
    else if (data[0] == 'S') {
      Sethome();
      
    }
  }

}