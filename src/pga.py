import time
import board
import busio
import adafruit_adxl34x
import math

# 初始化加速度计
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# 读取静止状态下的加速度计读数
time.sleep(3)  # 等待传感器稳定
offsets = accelerometer.acceleration
print("Offsets: %f %f %f" % offsets)

# 主循环，打印校准后的加速度计读数
while True:
    acceleration = accelerometer.acceleration
    calibrated_acceleration = (acceleration[0] - offsets[0], 
                               acceleration[1] - offsets[1], 
                               acceleration[2] - offsets[2])
    
    # 计算加速度的大小
    #magnitude = math.sqrt(sum([x**2 for x in calibrated_acceleration]))
    magnitude = math.sqrt(sum([abs(x)**2 for x in calibrated_acceleration]))
    
    # 更新并打印加速度
    print("加速度: %f" % magnitude)
    
    time.sleep(1)
