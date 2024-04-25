#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 实现功能：让GPIO21输出频率为40Hz，占空比为40%的PWM波
# 采用定时-翻转的方法实现。
import RPi.GPIO as GPIO
import time
# 参数设置
GPIO.setmode(GPIO.BCM)
PWM = 21
FREQUENCY = 40
DUTY = 0.4
GPIO.setup(PWM, GPIO.OUT) #GPIO21输出PWM波

# don't use too large freq
# 计算高电平和低电平的持续时间，单位是毫秒
def calc_delay_period(freq, duty):
    t = 1.0/freq
    ph = t*duty
    pl = t - ph
    return ph, pl

period_h, period_l = calc_delay_period(FREQUENCY, DUTY)

try:
    while True:
        GPIO.output(PWM, GPIO.HIGH)
        time.sleep(period_h)
        GPIO.output(PWM, GPIO.LOW)
        time.sleep(period_l)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
