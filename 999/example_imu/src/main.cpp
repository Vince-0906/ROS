#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);


void setup() {
  Serial.begin(115200);
  Wire.begin(18,19); // SDA, SCL
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 状态: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("计算偏移量, 不要移动 MPU6050"));
  delay(1000);
  mpu.calcOffsets(true,true); // gyro and accelero
  Serial.println("Done!\n");
  
}

unsigned long timer = 0;

void loop() {
  mpu.update();

  if(millis() - timer > 1000){ // print data every second
    Serial.print(F("温度: "));Serial.println(mpu.getTemp());
    Serial.print(F("加速度  X: "));Serial.print(mpu.getAccX());
    Serial.print("\tY: ");Serial.print(mpu.getAccY());
    Serial.print("\tZ: ");Serial.println(mpu.getAccZ());
  
    Serial.print(F("旋转      X: "));Serial.print(mpu.getGyroX());
    Serial.print("\tY: ");Serial.print(mpu.getGyroY());
    Serial.print("\tZ: ");Serial.println(mpu.getGyroZ());
  
    Serial.print(F("加速度角度 X: "));Serial.print(mpu.getAccAngleX());
    Serial.print("\tY: ");Serial.println(mpu.getAccAngleY());
    
    Serial.print(F("角度     X: "));Serial.print(mpu.getAngleX());
    Serial.print("\tY: ");Serial.print(mpu.getAngleY());
    Serial.print("\tZ: ");Serial.println(mpu.getAngleZ());
    Serial.println(F("=====================================================\n"));
    timer = millis();
  }

}
