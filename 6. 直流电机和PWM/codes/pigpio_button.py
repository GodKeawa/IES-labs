#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 按键控制电机转速，pigpio重构
import RPi.GPIO as GPIO
import pigpio
import time
pi = pigpio.pi()

# 设置按键以及输出引脚，BTN1和BTN2分别为减速和加速的按键
EA, I2, I1 = (13, 19, 26)
BTN1, BTN2 = (6, 5)
FREQUENCY = 50

# DUTYS是查找表，表示不同档位时占空比的值（0~100）；
DUTYS = (0, 20, 40, 60, 80, 100)
# duty_level是一个变量，表示当前占空比的档位，此处初始化为最大档位，即占空比100%
duty_level = len(DUTYS) - 1

# 设置各GPIO的输入输出模式和初始值。
# 其中I1和I2控制了电机的转向，如果发现实际情况与预期不符，只要在代码中或硬件连线上把I1和I2的值互换即可。
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1], GPIO.OUT)
GPIO.output([EA, I2], GPIO.LOW)
GPIO.output(I1, GPIO.HIGH)
GPIO.setup([BTN1, BTN2], GPIO.IN, pull_up_down = GPIO.PUD_UP)

# 使用GPIO库的pwm功能，创建一个PWM类的实例pwm
# 创建时需要指定两个参数：第一个参数指定输出引脚，第二个参数指定PWM波的频率。
# pwm = GPIO.PWM(EA, FREQUENCY)
pi.set_PWM_frequency(EA, FREQUENCY)

# 执行下面的代码之后，相应的引脚开始持续产生PWM输出。需要指定一个参数：占空比的值。范围是0~100。
# pwm.start(DUTYS[duty_level])
pi.set_PWM_range(EA, DUTYS[duty_level])
print("duty = %d" % DUTYS[duty_level])

# 检查按键是否被按下
def btn_pressed(btn):
    return GPIO.input(btn) == GPIO.LOW

# update_duty_level(delta)的delta为+1或者-1，表示占空比的档位增加或减少一档
# 据此算出新的占空比档位，然后调用ChangeDutyCycle(duty)方法更新占空比。参数duty同样是0~100之间的数。
def update_duty_level(delta):
    global duty_level
    old = duty_level
    duty_level = (duty_level + delta) % len(DUTYS)
    # pwm.ChangeDutyCycle(DUTYS[duty_level])
    pi.set_PWM_dutycycle(EA, DUTYS[duty_level])
    print("duty: %d --> %d" % (DUTYS[old], DUTYS[duty_level]))



btn1_released = True
btn2_released = True
try: # 保证程序在按下Ctrl+C之后能够正常退出
    # 无限的循环，用以检测按键是否按下，并进行相应的操作
    while True:
        if btn1_released:
            if btn_pressed(BTN1):
                time.sleep(0.01) # 按键消抖
                if btn_pressed(BTN1):
                    update_duty_level(-1)
                    btn1_released = False
        else:
            if not btn_pressed(BTN1):
                btn1_released = True
        if btn2_released:
            if btn_pressed(BTN2):
                time.sleep(0.01)
                if btn_pressed(BTN2):
                    update_duty_level(1)
                    btn2_released = False
        else:
            if not btn_pressed(BTN2):
                btn2_released = True
except KeyboardInterrupt:
    pass
# 在程序结束前，不仅要调用GPIO.cleanup()，还要调用pwm.stop()来停止PWM输出
# 否则程序结束后，这个PWM会持续输出，造成不必要的能耗以及以外损坏的风险。
# pwm.stop()
pi.set_PWM_dutycycle(EA, 0)
GPIO.cleanup()
                