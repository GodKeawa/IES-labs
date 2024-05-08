# 库引入
import RPi.GPIO as GPIO
import pigpio
import time  # 引入时间库
import numpy
import matplotlib.pyplot as plt

pi = pigpio.pi()
# 接口定义与初始化
# 设置各个GPIO口与pwm
EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50  # 50Hz
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.setup([LS, RS], GPIO.IN)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)

pi.set_PWM_frequency(EA, FREQUENCY)
pi.set_PWM_frequency(EB, FREQUENCY)
pi.set_PWM_range(EA, 100)
pi.set_PWM_range(EB, 100)
pi.set_PWM_dutycycle(EA, 0)
pi.set_PWM_dutycycle(EB, 0)

lcounter = 0
rcounter = 0


# event detect函数
# 检测信号的上升沿和下降沿，并在检测到边缘时执行线程回调函数
def my_callback(channel):  # 定义回调函数
    global lcounter  # 引入全局变量
    global rcounter
    if channel == LS:  # 判断是哪个通道触发了回调函数
        lcounter += 1  # 计数器加1
    elif channel == RS:
        rcounter += 1



i = 0
x = []
y1 = []
y2 = []
while i <= 20:
    # 主函数每隔3秒增加一次pwm的占空比（本例中步长为5%）。
    # 并读取一次新占空比下的两个speed，存入两个数组中。
    x.append(5 * i)
    pi.set_PWM_dutycycle(EA, 5 * i)
    pi.set_PWM_dutycycle(EB, 5 * i)

    time.sleep(2) #等待加速
    rcounter = 0
    lcounter = 0
    # 添加两个边沿检测，并调回my_callback
    # GPIO.RISING 也可以使用GPIO.FALLING、GPIO.BOTH 对边缘进行检测
    GPIO.add_event_detect(LS, GPIO.RISING, callback=my_callback)
    GPIO.add_event_detect(RS, GPIO.RISING, callback=my_callback)
    time.sleep(0.1)
    # 终止event_detect
    GPIO.remove_event_detect(LS)
    GPIO.remove_event_detect(RS)
    y1.append(lcounter / 58.5)
    y2.append(rcounter / 58.5)
    i = i + 1

# 显示出lspeed与rspeed关于pwm的关系图像。
plt.plot(x, y1, "-o")
plt.plot(x, y2, "-*")
pi.set_PWM_dutycycle(EA, 0)
pi.set_PWM_dutycycle(EB, 0)

GPIO.cleanup()
plt.show()
