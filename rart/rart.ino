String myString;
void setup() {
  Serial.begin(9600);
  
}
void loop() {

   Serial.println("hello");
//   if (!Serial.available()) {  //檢查 RX 緩衝器, 直到有資料進來
//    }
//    myString = Serial.read();
////    delay(500);
//    Serial.println(myString);
   delay(500);
}
