#include "Keyboard.h"
const int b1 = 2;
const int b2 = 3;
const int b3 = 4;
const int b4 = 5;
const int b5 = 9;


void setup() {
  
pinMode(b1, INPUT_PULLUP);
pinMode(b2, INPUT_PULLUP);
pinMode(b3, INPUT_PULLUP);
pinMode(b4, INPUT_PULLUP);
pinMode(b5, INPUT_PULLUP);
Keyboard.begin();

}

void loop() {
 
if(!digitalRead(b1)){
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
   delay(200);
}
if(!digitalRead(b2)){
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press('q');
  Keyboard.releaseAll();
  delay(200);
}
if(!digitalRead(b3)){
  Keyboard.press('s');
  Keyboard.press('d');
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(200);
}
if(!digitalRead(b4)){
  Keyboard.press('r');
  Keyboard.press('b');
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(200);
}
if(!digitalRead(b5)){
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press('o');
  Keyboard.releaseAll();
  delay(200);
}
}
