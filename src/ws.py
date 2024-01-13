import asyncio
import websockets
import time
import board
import busio
import adafruit_adxl34x
import math
from collections import deque

# 初始化加速度计
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# 读取静止状态下的加速度计读数
time.sleep(3)  # 等待传感器稳定
offsets = accelerometer.acceleration

# 初始化滑动平均滤波器
window_size = 10
window = deque(maxlen=window_size)

async def echo(websocket, path):
    while True:
        acceleration = accelerometer.acceleration
        calibrated_acceleration = (acceleration[0] - offsets[0], 
                                   acceleration[1] - offsets[1], 
                                   acceleration[2] - offsets[2])
        magnitude = math.sqrt(sum([abs(x)**2 for x in calibrated_acceleration]))

        # 更新滑动窗口
        window.append(magnitude)
        avg_magnitude = sum(window) / len(window)

        # 检测地震
        if avg_magnitude > 1.0:  # 这个阈值可能需要调整
            #await websocket.send(str(avg_magnitude))
            await websocket.send(f"Earthquake detected! Acceleration: {avg_magnitude}")
        else:
            await websocket.send(str(avg_magnitude))
        time.sleep(1)

start_server = websockets.serve(echo, "0.0.0.0", 8765)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"An error occurred: {e}")
