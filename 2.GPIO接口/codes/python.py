# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 首先调用GPIO.setmode函数来确定引脚的模式。
# 在RPi.GPIO包中定义GPIO针脚的两种模式：BCM模式和BOARD模式。
GPIO.setmode(GPIO.BCM)
led = 21
GPIO.setup(led, GPIO.OUT)
print("输出高电平")
GPIO.output(led, GPIO.HIGH)
time.sleep(5)
GPIO.output(led, GPIO.LOW)
print("输出低电平")

# GPIO.cleanup()函数清除掉之前GPIO.setup()设置的状态，恢复所有使用过的GPIO状态为输入，避免由于短路意外损坏树莓派。
# 注意，该操作仅会清理你的代码使用过的GPIO通道。退出程序之前一定要调用，否则下次调用该GPIO的时候会报错。
GPIO.cleanup()
