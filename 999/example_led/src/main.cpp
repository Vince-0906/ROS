#include <Arduino.h>
void setup()
{
    pinMode(2, OUTPUT);
}
void loop()
{
    digitalWrite(2, HIGH); //打开LED
    delay(1000);
    digitalWrite(2, LOW); //关闭LED
    delay(1000);
}