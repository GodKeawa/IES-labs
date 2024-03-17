# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 同上初始化
GPIO.setmode(GPIO.BCM)
led = 21
bt = 20
GPIO.setup(led, GPIO.OUT)
GPIO.setup(bt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ledStatus = True


def my_callback(channel):  # 事件函数/回调函数
    print("button pressed")  # 输出
    global ledStatus
    ledStatus = not ledStatus
    if ledStatus:  # 控制LED
        GPIO.output(led, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.LOW)


# 添加一个事件检测，检测条件为GPIO20的下降沿，即按键被按下
# 设置bouncetime参数为程序提供去抖
GPIO.add_event_detect(bt, GPIO.FALLING, callback=my_callback, bouncetime=200)

try:  # 循环输出并提供程序结束方法
    while True:
        print("I LOVE Raspberry Pi")
        time.sleep(2)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
