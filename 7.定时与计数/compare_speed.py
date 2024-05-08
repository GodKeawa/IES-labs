# 库引入
import RPi.GPIO as GPIO
import pigpio
import time  # 引入时间库
import threading  # 引入线程库
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

# 多线程模式
pi.set_PWM_dutycycle(EA, 0)
pi.set_PWM_dutycycle(EB, 0)

lspeed = 0
rspeed = 0
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


# 测速函数
def getspeed():
    global rspeed  # 设置全局变量lspeed、rspeed，用于向主函数传递电机速度
    global lspeed
    # lcounter与rcounter用于记录从上一次被清零开始，两个霍尔传感器收到了多少个方波
    global lcounter
    global rcounter
    # 添加两个边沿检测，并调回my_callback
    # GPIO.RISING 也可以使用GPIO.FALLING、GPIO.BOTH 对边缘进行检测
    GPIO.add_event_detect(LS, GPIO.RISING, callback=my_callback)
    GPIO.add_event_detect(RS, GPIO.RISING, callback=my_callback)
    while True:
        # 每隔一秒读取一次counter值并转换成速度传递给相应的speed，然后将counter清零。
        rspeed = rcounter / 585.0
        # “/585.0”是因为轮子转一圈会有585个脉冲，用“.0”是为了防止speed被自动取整
        lspeed = lcounter / 585.0
        rcounter = 0
        lcounter = 0
        time.sleep(1)


thread1 = threading.Thread(target=getspeed)  # 创建新线程
thread1.start()  # 启动线程
# 它会不停的统计光电门输入的上升沿，并每隔一秒把全局变量更新为前一秒的速度。单位：圈/秒
# threading没有提供停止线程的方法，关闭图像后可以使用⌃+z结束程序

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

    time.sleep(3)
    y1.append(lspeed)
    y2.append(rspeed)
    i = i + 1

pi.set_PWM_dutycycle(EA, 0)
pi.set_PWM_dutycycle(EB, 0)

GPIO.remove_event_detect(LS)
GPIO.remove_event_detect(RS)

# 单线程模式
# 新测速函数
def new_getspeed():
    # lcounter与rcounter用于记录从上一次被清零开始，两个霍尔传感器收到了多少个方波
    global lcounter
    global rcounter
    # 添加两个边沿检测，并调回my_callback
    # GPIO.RISING 也可以使用GPIO.FALLING、GPIO.BOTH 对边缘进行检测
    GPIO.add_event_detect(LS, GPIO.RISING, callback=my_callback)
    GPIO.add_event_detect(RS, GPIO.RISING, callback=my_callback)
    time.sleep(0.1)
    # 终止event_detect
    GPIO.remove_event_detect(LS)
    GPIO.remove_event_detect(RS)


i = 0
new_x = []
new_y1 = []
new_y2 = []
while i <= 20:
    # 主函数每隔3秒增加一次pwm的占空比（本例中步长为5%）。
    # 并读取一次新占空比下的两个speed，存入两个数组中。
    new_x.append(5 * i)
    pi.set_PWM_dutycycle(EA, 5 * i)
    pi.set_PWM_dutycycle(EB, 5 * i)

    time.sleep(1.5)  # 等待加速
    rcounter = 0
    lcounter = 0
    getspeed()  # 运行0.1秒event_detect
    time.sleep(1.4)
    new_y1.append(lcounter / 585.0)
    new_y2.append(rcounter / 585.0)
    i = i + 1

pi.set_PWM_dutycycle(EA, 0)
pi.set_PWM_dutycycle(EB, 0)

GPIO.cleanup()

# 显示出lspeed与rspeed关于pwm的关系图像。
plt.subplot(1, 3, 1)
plt.plot(x, y1, "-o")
plt.plot(x, y2, "-*")

plt.subplot(1,3,2)
plt.plot(new_x, new_y1, "-o")
plt.plot(new_x, new_y2, "-*")


plt.subplot(1, 3, 3)
plt.plot(x,new_x,"-o") #基准线 y=x
plt.plot(y1,new_y1,"-o")
plt.plot(y2,new_y2,"-o")

plt.show()
