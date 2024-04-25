#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 键盘控制电机，pigpio重构
import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi()
# GPIO引脚设置，可以在这里反转引脚设置来让电机反转
EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)
# 常量设置
FREQUENCY = 50
DUTYS_A = {'w':20,'a':0, 's':0, 'd':20}
DUTYS_B = {'w':20,'a':20,'s':0, 'd':0 }
EXPRESSIONS = {'w':'move forward!',
               'a':'turn left!',
               's':'stop!',
               'd':'turn right!'}
# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)
# 左右轮PWM设置
# pwma = GPIO.PWM(EA, FREQUENCY)
# pwmb = GPIO.PWM(EB, FREQUENCY)
pi.set_PWM_frequency(EA, FREQUENCY)
pi.set_PWM_frequency(EB, FREQUENCY)
# 初始化为不动
# pwma.start(DUTYS_A['s'])
# pwmb.start(DUTYS_B['s'])
pi.set_PWM_dutycycle(EA, DUTYS_A['s'])
pi.set_PWM_dutycycle(EB, DUTYS_B['s'])

print("ready!")

while True:
    cmd = input("command >> ")
    if cmd == 'q':
        # pwma.stop()
        # pwmb.stop()
        pi.set_PWM_dutycycle(EA, 0)
        pi.set_PWM_dutycycle(EB, 0)
        GPIO.cleanup()
        break
    elif (cmd=='w') or (cmd=='a') or (cmd=='s') or (cmd=='d'):
        # pwma.ChangeDutyCycle(DUTYS_A[cmd])
        # pwmb.ChangeDutyCycle(DUTYS_B[cmd])
        pi.set_PWM_dutycycle(EA, DUTYS_A[cmd])
        pi.set_PWM_dutycycle(EB, DUTYS_B[cmd])
        print(EXPRESSIONS[cmd])
    else:
        pass
