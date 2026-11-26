#include <Arduino.h>
#include <Wire.h>
#include <AS5600.h>
#include <TCA9548.h>

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
int namcham = 13;
int CB1;
int CB2;
int CB3;
int sethome;
int start_mode = 0;
int stop_mode = 0;
int DHT = 0;
int DHN = 0;
int TTG = 0;
float goc_dc1 = 0.0;
float goc_dc2 = 0.0;
float goc_dc3 = 0.0;
float goc_quakhu_dc1 = 0.0;
float goc_quakhu_dc2 = 0.0;
float goc_quakhu_dc3 = 0.0;
float goc_hientai_dc1 = 0.0;
float goc_hientai_dc2 = 0.0;
float goc_hientai_dc3 = 0.0;

// KHAI BAO CAM BIEN
TCA9548 tca(0x70);
AS5600 encoder;

// KENH TCA9548A
const uint8_t kenh[3] = {5, 6, 7};

// TI SO TRUYEN TUNG KHOP
// Neu cam bien gan truc khop: doi thanh 1.0
float tiSoTruyen[3] = {3.75f, 3.75f, 3.75f};

// CHIEU QUAY CUA TUNG KHOP
int chieuGoc[3] = {1, -1, -1};

// CAC BIEN LUU GOC
float gocAS5600[3] = {0, 0, 0};
float gocTruoc[3] = {0, 0, 0};
float gocTichLuy[3] = {0, 0, 0};
float gocHome[3] = {0, 0, 0};
float gocKhop[3] = {0, 0, 0};
// TRANG THAI CAM BIEN
bool daDocLanDau[3] = {false, false, false};

bool daHome = false;


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
  pinMode(limitx , INPUT_PULLDOWN);
  pinMode(limity , INPUT);
  pinMode(limitz , INPUT);
  pinMode(namcham, OUTPUT);
  // A4988: 1/16 microstep
  digitalWrite(MS1_dc1_3, HIGH);
  digitalWrite(MS2_dc1_3, HIGH);
  digitalWrite(MS3_dc1_3, HIGH);
  // A4988: full step
  digitalWrite(MS1_dc2, LOW);
  digitalWrite(MS2_dc2, LOW);
  digitalWrite(MS3_dc2, LOW);

  // KHOI TAO I2C ESP32
  Wire.begin(21, 22);
  Wire.setClock(100000);

  delay(500);

  // KHOI TAO TCA9548A
  if (!tca.begin()) {
    Serial.println("Khong tim thay TCA9548A!");
    return;
  }


  Serial.println("KHOI TAO 3 CAM BIEN AS5600");

  // KIEM TRA TUNG CAM BIEN
  for (int i = 0; i < 3; i++) {

    tca.selectChannel(kenh[i]);

    bool ok = encoder.begin();

    Serial.print("Khop ");
    Serial.print(i + 1);
    Serial.print(" - Kenh ");
    Serial.print(kenh[i]);

    if (ok && encoder.detectMagnet()) {
      Serial.println(": OK");
    }
    else {
      Serial.println(": LOI / KHONG CO NAM CHAM");
    }
  }
  // Luôn enable driver
  digitalWrite(ena, LOW);

  digitalWrite(namcham,LOW);
}

bool docgoc(int i, float &goc) {

  // Chon kenh TCA
  tca.selectChannel(kenh[i]);
  // Doc goc
  uint16_t raw = encoder.rawAngle();

  goc = raw * 360.0f / 4096.0f;

  return true;
}

bool capnhatgoc(int i) {

  float goc;

  docgoc(i, goc);
  gocAS5600[i] = goc;

  // DOC LAN DAU
  if (!daDocLanDau[i]) {
    gocTruoc[i] = goc;
    daDocLanDau[i] = true;
    return true;
  }

  // TINH GOC THAY DOI
  float delta = goc - gocTruoc[i];

  // XU LY KHI VUOT 0 / 360
  if (delta > 180.0f) {
    delta -= 360.0f;
  }
  else if (delta < -180.0f) {
    delta += 360.0f;
  }

  // CONG DON GOC QUAY
  gocTichLuy[i] += delta;

  // CAP NHAT GOC CU
  gocTruoc[i] = goc;

  return true;
}


void Sethome(){
  digitalWrite(ena,LOW);
  delayMicroseconds(10);
  digitalWrite(dir2, HIGH);
  for(int i =0 ; i<188; i++){
    stop();
    if(stop_mode > 0){
      return;
    }
    CB2 = digitalRead(limity);
    if(CB2 == 1){
      break;
    }
    digitalWrite(step2,HIGH);
    delay(18);
    digitalWrite(step2,LOW);
    delay(18);

  }
  digitalWrite(dir2, LOW);
  for(int i = 0 ; i<376; i++){
    stop();
    if(stop_mode > 0){
      return;
    }
    CB2 = digitalRead(limity);
    if(CB2 == 1){
      break;
    }
    digitalWrite(step2,HIGH);
    delay(18);
    digitalWrite(step2,LOW);
    delay(18);

  }
  digitalWrite(dir3, LOW);
  for(int i = 0; i< 3000; i++){
    stop();
    if(stop_mode > 0){
      return;
    }
    CB3 = digitalRead(limitz);
    if(CB3 == 1){
      break;
    }
    digitalWrite(step3,HIGH);
    delayMicroseconds(1000);
    digitalWrite(step3,LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(dir3, HIGH);
  for(int i = 0; i< 6000; i++){
    stop();
    if(stop_mode > 0){
      return;
    }
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
    stop();
    if(stop_mode > 0){
      return;
    }
    CB1 = digitalRead(limitx);
    Serial.println(CB1);
    if(CB1 == 1){
      break;
    }
    digitalWrite(step1,HIGH);
    delayMicroseconds(1500);
    digitalWrite(step1,LOW);
    delayMicroseconds(1500);
  }
  digitalWrite(dir1,LOW);
  for(int i = 0; i< 6000; i++){
    stop();
    if(stop_mode > 0){
      return;
    }
    CB1 = digitalRead(limitx);
    Serial.println(CB1);
    if(CB1 == 1){
      break;
    }
    digitalWrite(step1,HIGH);
    delayMicroseconds(1500);
    digitalWrite(step1,LOW);
    delayMicroseconds(1500);
    
  }
}
void Move_to_angle(unsigned long nstepx, unsigned long nstepy, unsigned long nstepz, float goc1,float goc2,float goc3){
  if (TTG == 0){
    dc1(goc1, nstepx);
    dc3(goc3, nstepz);
    dc2(goc2, nstepy);
  }
  else{
    if(goc2 < 0) {
      dc3(goc3, nstepz);
      dc1(goc1, nstepx);
      dc2(goc2, nstepy);
      
    }
    else{
      dc2(goc2, nstepy);
      dc1(goc1, nstepx);
      dc3(goc3, nstepz);
    }
   
  }
  if(daHome){
    TTG = 1;
  }
  
  
}
void dc1(float goc1, unsigned long nstepx){
  if(goc1>0){
    digitalWrite(dir1,HIGH);
  }
  else{
    digitalWrite(dir1,LOW);
  }
  for(int i = 0; i<nstepx; i++){
    digitalWrite(step1, HIGH);
    delayMicroseconds(1500);
    digitalWrite(step1, LOW);
    delayMicroseconds(1500);
    stop();
    if(stop_mode > 0){
      return;
    }
    else{
      if(i % 7 == 0){
        capnhatgoc(0);
        float gocdongco = gocTichLuy[0] - gocHome[0];
        gocKhop[0] = chieuGoc[0] * gocdongco / tiSoTruyen[0];
        Serial.print("khop 1: ");
        Serial.print(gocKhop[0],2);
        Serial.print(" do");
        Serial.println("");
      }
      
    }

    
  }
}
void dc2(float goc2, unsigned long nstepy){
  if(goc2>0){
    digitalWrite(dir2,HIGH);
  }
  else{
    digitalWrite(dir2,LOW);
  }
  for(int i =0; i<nstepy; i++){
    digitalWrite(step2, HIGH);
    delay(18);
    digitalWrite(step2, LOW);
    delay(18);
    stop();
    if(stop_mode > 0){
      return;
    }
    else{
      capnhatgoc(1);
      float gocdongco = gocTichLuy[1] - gocHome[1];
      gocKhop[1] = chieuGoc[1] * gocdongco / tiSoTruyen[1];
      Serial.print("khop 2: ");
      Serial.print(gocKhop[1],2);
      Serial.print(" do");
      Serial.println("");
    }
    
  }
}
void dc3(float goc3, unsigned long nstepz){
  if(goc3>0){
    digitalWrite(dir3,LOW);
  }
  else{
    digitalWrite(dir3,HIGH);
  }
  for(int i =0; i<nstepz; i++){
    digitalWrite(step3, HIGH);
    delayMicroseconds(1000);
    digitalWrite(step3, LOW);
    delayMicroseconds(1000);
    stop();
    if(stop_mode > 0){
      return;
    }
    else{
      if(i%10==0){
        capnhatgoc(2);
        float gocdongco = gocTichLuy[2] - gocHome[2];
        gocKhop[2] = chieuGoc[2] * gocdongco / tiSoTruyen[2];
        Serial.print("khop 3: ");
        Serial.print(gocKhop[2],2);
        Serial.print(" do");
        Serial.println("");
      }
      
    }
    
  }
}

void capnhatgocmoi(){
  for(int i =0;i<3;i++){
    capnhatgoc(i);
    float gocdongco = gocTichLuy[i] - gocHome[i];
    gocKhop[i] = chieuGoc[i] * gocdongco / tiSoTruyen[i];
    Serial.print("khop ");
    Serial.print(i+1);
    Serial.print(': ');
    Serial.print(gocKhop[i],2);
    Serial.print(" do");
    Serial.println("");
  }
}
void fc_namcham(bool state) {
  digitalWrite(namcham,state);
}
void stop(){
  while(Serial.available()){
    char data = Serial.read();
    if(data == 'O'){
      Serial.println("Tat dong co");
      digitalWrite(ena,HIGH);
      Serial.println("Robot mode: OFF");
      start_mode = 0;
      stop_mode++;
      DHT = 0;
      for(int i = 0;i < 3;i++){
        gocAS5600[i] = 0;
        gocTruoc[i] = 0;
        gocTichLuy[i] = 0;
        gocHome[i] = 0;
        gocKhop[i] = 0;
        daDocLanDau[i] = false;
      }
      
      daHome = false;
    }
  }
}
void loop() {
  while(Serial.available()){
    String data = Serial.readString();
    delayMicroseconds(5);
    if (data[0] == 'H') {
      fc_namcham(HIGH);
    }
    else if (data[0] == 'T') {
      fc_namcham(LOW);
    }
    else if (data[0]=='D'){
      capnhatgocmoi();
    }
    else if (data[0] == 'O') {
      Serial.println("Tat dong co");
      digitalWrite(ena,HIGH);
      Serial.println("Robot mode: OFF");
      start_mode = 0;
      stop_mode++;
      DHT = 0;
      for(int i = 0;i < 3;i++){
        gocAS5600[i] = 0;
        gocTruoc[i] = 0;
        gocTichLuy[i] = 0;
        gocHome[i] = 0;
        gocKhop[i] = 0;
        daDocLanDau[i] = false;
      }
      daHome = false;
    }
    else if ((data[0] == 'S') && (start_mode == 0))  {
      Serial.println("Dang set home");
      start_mode++;
      stop_mode = 0;
      DHT = 0;
      TTG=0;
      goc_dc1 = 0.0;
      goc_dc2 = 0.0;
      goc_dc3 = 0.0;
      goc_quakhu_dc1 = 0.0;
      goc_quakhu_dc2 = 0.0;
      goc_quakhu_dc3 = 0.0;
      goc_hientai_dc1 = 0.0;
      goc_hientai_dc2 = 0.0;
      goc_hientai_dc3 = 0.0;
      Sethome();
      delay(3500);
      if(stop_mode == 0){
        for(int i = 0; i<3;i++){
        capnhatgoc(i);
        }
        for (int i = 0; i < 3; i++) {
          gocHome[i] = gocTichLuy[i];
        }
        daHome = true;
        Serial.println("Hoan thanh sethome!");
        Serial.println("Robot mode: ON");
      }
      else{
        Serial.println("Sethome khong thanh cong!");
        Serial.println("Robot mode: OFF");
      }
      
    }
    else if((data[0] == 'F') && start_mode == 1){
      int index_A = data.indexOf('A');
      int index_B = data.indexOf('B');
      int index_C = data.indexOf('C');
      if (index_A >1 && index_B > index_A && index_C > index_B){
        goc_hientai_dc1 = data.substring(1,index_A).toFloat();
        goc_hientai_dc2 = data.substring(index_A + 1,index_B).toFloat();
        goc_hientai_dc3 = data.substring(index_B + 1,index_C).toFloat();
        goc_dc1 = goc_hientai_dc1 - goc_quakhu_dc1;
        goc_dc2 = goc_hientai_dc2 - goc_quakhu_dc2;
        goc_dc3 = goc_hientai_dc3 - goc_quakhu_dc3;
        Serial.println(goc_dc1);
        Serial.println(goc_dc2);
        Serial.println(goc_dc3);
        unsigned long nstepx = ((abs(goc_dc1))/(1.8/16)) * 3.75;
        unsigned long nstepy = ((abs(goc_dc2))/(1.8)) * 3.75;
        unsigned long nstepz = ((abs(goc_dc3))/(1.8/16)) * 3.75;
        Serial.println(nstepx);
        Serial.println(nstepy);
        Serial.println(nstepz);
        Move_to_angle(nstepx,nstepy,nstepz,goc_dc1,goc_dc2,goc_dc3);
        capnhatgocmoi();
        goc_quakhu_dc1 = goc_hientai_dc1;
        goc_quakhu_dc2 = goc_hientai_dc2;
        goc_quakhu_dc3 = goc_hientai_dc3;
      }
    }
  }

}
