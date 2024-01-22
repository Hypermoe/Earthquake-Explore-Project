import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import board
import busio
import adafruit_adxl34x

# 创建一个新的图形和一个子图
fig, ax = plt.subplots()

# 设置y轴的范围为-3000到3000
plt.ylim(-5, 5)

# 初始化一个空的y值列表
ydata = [0] * 50
line, = plt.plot(ydata)

# 更新函数
def update(data):
    # 将数据添加到ydata的末尾
    ydata.append(data)
    # 删除ydata的第一个元素，以保持列表长度不变
    del ydata[0]
    line.set_ydata(ydata)
    return line,

# 生成函数
def data_gen():
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    while True:
        yield accelerometer.acceleration[0]

# 创建动画
ani = animation.FuncAnimation(fig, update, data_gen, interval=100)

plt.show()
