import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import board
import busio
import adafruit_adxl34x
from datetime import datetime, timedelta

# 创建一个新的图形和一个子图
fig, ax = plt.subplots()

# 初始化一个空的y值列表和xdata列表
interval = 233  # 你可以根据需要修改这个值
time_window = 120  # 时间窗口的值，单位是秒
num_points = int(time_window * 10000 / interval)  # 根据interval动态计算数据点的数量
ydata = [0]
xdata = [datetime.now()]

line, = plt.plot(xdata, ydata)

# 更新函数
def update(data):
    # 将数据添加到ydata和xdata的末尾
    ydata.append(data)
    xdata.append(datetime.now())
    # 如果数据点的数量超过了num_points，就删除ydata和xdata的第一个元素，以保持列表长度不变
    if len(ydata) > num_points:
        del ydata[0]
        del xdata[0]
    line.set_ydata(ydata)
    line.set_xdata(xdata)
    # 更新x轴的范围
    plt.xlim([datetime.now() - timedelta(seconds=time_window), datetime.now()])  # x轴范围是time_window秒

    # 自适应调整y轴
    if ydata:  # 避免在ydata为空时调用max()和min()
        y_max = max(0, max(ydata))
        y_min = min(0, min(ydata))
        y_range = max(abs(y_max), abs(y_min))
        plt.ylim(-y_range - 1, y_range + 1)
    
    return line,

# 生成函数
def data_gen():
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    while True:
        yield accelerometer.acceleration[0]

# 创建动画，每interval毫秒刷新一次
ani = animation.FuncAnimation(fig, update, data_gen, interval=interval)  # 注意这里的interval

# 在图形开始时立即更新一次，然后删除初始数据
update(next(data_gen()))
del ydata[0]
del xdata[0]

plt.show()
