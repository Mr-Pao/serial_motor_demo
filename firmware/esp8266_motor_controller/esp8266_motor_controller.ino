#include <Wire.h>

#define Motor_model_ADDR 0x60

#define MOTOR_TYPE_REG        0x00
#define MOTOR_DeadZONE_REG    0x02
#define MOTOR_PluseLine_REG   0x04
#define MOTOR_PlusePhase_REG  0x06
#define WHEEL_DIA_REG         0x08
#define SPEED_Control_REG     0x0C
#define PWM_Control_REG       0x14

#define READ_TEN_M1Enconer_REG 0x1C
#define READ_TEN_M2Enconer_REG 0x1E

void i2cWrite(uint8_t devAddr, uint8_t regAddr, uint8_t length, uint8_t *data) {
  Wire.beginTransmission(devAddr);
  Wire.write(regAddr);
  for (uint8_t i = 0; i < length; i++) {
    Wire.write(data[i]);
  }
  int result = Wire.endTransmission();
  if (result != 0) {
    Serial.printf("I2C Write Error: %d (addr=0x%02X, reg=0x%02X)\n", result, devAddr, regAddr);
  }
}

void i2cRead(uint8_t devAddr, uint8_t regAddr, uint8_t length, uint8_t *data) {
  Wire.beginTransmission(devAddr);
  Wire.write(regAddr);
  Wire.endTransmission(false);
  Wire.requestFrom(devAddr, length);
  for (uint8_t i = 0; i < length; i++) {
    data[i] = Wire.read();
  }
}

void setup() {
  Wire.begin();
  Serial.begin(115200);
  
  delay(500);
  Serial.println("=== ESP8266 Motor Controller ===");
  Serial.println("Initializing I2C...");
  
  // 扫描 I2C 设备
  Serial.println("Scanning I2C bus...");
  byte error, address;
  int nDevices = 0;
  for(address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.printf("I2C device found at address 0x%02X\n", address);
      nDevices++;
    }
  }
  if (nDevices == 0) {
    Serial.println("NO I2C devices found! Check wiring!");
  } else {
    Serial.printf("Found %d I2C device(s)\n", nDevices);
  }
  
  // 初始化电机驱动
  Serial.println("Initializing motor driver...");
  uint8_t motor_type = 0x01;
  i2cWrite(Motor_model_ADDR, MOTOR_TYPE_REG, 1, &motor_type);
  
  uint8_t deadzone[2] = {0x00, 0x10};
  i2cWrite(Motor_model_ADDR, MOTOR_DeadZONE_REG, 2, deadzone);
  
  uint8_t pulseline[2] = {0x00, 0x0B};
  i2cWrite(Motor_model_ADDR, MOTOR_PluseLine_REG, 2, pulseline);
  
  uint8_t phase[2] = {0x00, 0x1E};
  i2cWrite(Motor_model_ADDR, MOTOR_PlusePhase_REG, 2, phase);
  
  float wheel_dia = 0.05;
  uint8_t dia_bytes[4];
  memcpy(dia_bytes, &wheel_dia, sizeof(float));
  i2cWrite(Motor_model_ADDR, WHEEL_DIA_REG, 4, dia_bytes);
  
  // 停止电机
  uint8_t stop_pwm[8] = {0,0,0,0,0,0,0,0};
  i2cWrite(Motor_model_ADDR, PWM_Control_REG, 8, stop_pwm);
  
  Serial.println("Motor driver ready!");
  Serial.println("Commands: SPEED:x,y,z,w | PWM:x,y,z,w | STOP | STATUS | SCAN");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd.startsWith("SPEED:")) {
      String speed_str = cmd.substring(6);
      int values[4] = {0,0,0,0};
      
      if (speed_str.indexOf(',') != -1) {
        int idx = 0;
        int start = 0;
        for (int i = 0; i < speed_str.length(); i++) {
          if (speed_str[i] == ',' || i == speed_str.length() - 1) {
            int end = (i == speed_str.length() - 1) ? i + 1 : i;
            values[idx] = speed_str.substring(start, end).toInt();
            idx++;
            start = i + 1;
            if (idx >= 4) break;
          }
        }
      } else {
        int speed = speed_str.toInt();
        for (int i = 0; i < 4; i++) values[i] = speed;
      }
      
      uint8_t speed_data[8];
      for (int i = 0; i < 4; i++) {
        speed_data[i*2] = (values[i] >> 8) & 0xff;
        speed_data[i*2+1] = values[i] & 0xff;
      }
      i2cWrite(Motor_model_ADDR, SPEED_Control_REG, 8, speed_data);
      Serial.printf("Speed: %d,%d,%d,%d\n", values[0],values[1],values[2],values[3]);
      
    } else if (cmd.startsWith("PWM:")) {
      String pwm_str = cmd.substring(4);
      int values[4] = {0,0,0,0};
      
      if (pwm_str.indexOf(',') != -1) {
        int idx = 0;
        int start = 0;
        for (int i = 0; i < pwm_str.length(); i++) {
          if (pwm_str[i] == ',' || i == pwm_str.length() - 1) {
            int end = (i == speed_str.length() - 1) ? i + 1 : i;
            values[idx] = pwm_str.substring(start, end).toInt();
            idx++;
            start = i + 1;
            if (idx >= 4) break;
          }
        }
      } else {
        int pwm = pwm_str.toInt();
        for (int i = 0; i < 4; i++) values[i] = pwm;
      }
      
      uint8_t pwm_data[8];
      for (int i = 0; i < 4; i++) {
        pwm_data[i*2] = (values[i] >> 8) & 0xff;
        pwm_data[i*2+1] = values[i] & 0xff;
      }
      i2cWrite(Motor_model_ADDR, PWM_Control_REG, 8, pwm_data);
      Serial.printf("PWM: %d,%d,%d,%d\n", values[0],values[1],values[2],values[3]);
      
    } else if (cmd == "STOP") {
      uint8_t stop_pwm[8] = {0,0,0,0,0,0,0,0};
      i2cWrite(Motor_model_ADDR, PWM_Control_REG, 8, stop_pwm);
      Serial.println("Stopped");
      
    } else if (cmd == "STATUS") {
      uint8_t buf[2];
      i2cRead(Motor_model_ADDR, READ_TEN_M1Enconer_REG, 2, buf);
      int16_t enc1 = (buf[0] << 8) | buf[1];
      i2cRead(Motor_model_ADDR, READ_TEN_M2Enconer_REG, 2, buf);
      int16_t enc2 = (buf[0] << 8) | buf[1];
      Serial.printf("Encoders: M1=%d, M2=%d\n", enc1, enc2);
      
    } else if (cmd == "SCAN") {
      Serial.println("Scanning I2C bus...");
      byte error, address;
      int nDevices = 0;
      for(address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        error = Wire.endTransmission();
        if (error == 0) {
          Serial.printf("Found at 0x%02X\n", address);
          nDevices++;
        }
      }
      Serial.printf("Total: %d devices\n", nDevices);
      
    } else {
      Serial.println("Unknown command");
    }
  }
  delay(10);
}