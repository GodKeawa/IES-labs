# Digital to Analog
# TLC5620

# TLC5620           Pi
# CLK(7)    -----   Pin37
# DATA(6)   -----   Pin38
# LOAD(8)   -----   Pin40

# VDD(14)   -----   5V
# GND(1)    -----   GND
# LDAC(13)  -----   GND
# REFA(2)   -----   3.3V
# DACA(12)  -----   Analog Output

# 用Pin37，Pin38，Pin40分别控制CLK，DATA，LOAD引脚。
# 引脚LDAC接地。
# 电源电压VDD接5V。
# 令A1A0=00，选择DACA输出模拟信号。

import RPi.GPIO as GPIO

DAC_CLK=26 #37
DAC_DATA=20 #38
DAC_LOAD=21 #40

# 设置引脚模式（兼容自定义引脚编号）
def setup(clk=26,data=20,load=21): #37,38,40
    global DAC_CLK,DAC_DATA,DAC_LOAD
    DAC_CLK=clk
    DAC_DATA=data
    DAC_LOAD=load
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DAC_CLK,GPIO.OUT)
    GPIO.setup(DAC_DATA,GPIO.OUT)
    GPIO.setup(DAC_LOAD,GPIO.OUT)

# 清除引脚设置
def destroy():
    GPIO.cleanup()
    
# 发送一个数据
def SendOneData(num,a1=0,a0=0,rng=0):
    GPIO.output(DAC_LOAD,1) # Load设置为高电平准备输入
    # 依据协议选择通道
    GPIO.output(DAC_DATA,a1)
    GPIO.output(DAC_CLK,1)
    GPIO.output(DAC_CLK,0)   # Output A1
    
    GPIO.output(DAC_DATA,a0)
    GPIO.output(DAC_CLK,1)
    GPIO.output(DAC_CLK,0)   # Output A0
    # 写入RNG
    GPIO.output(DAC_DATA,rng)
    GPIO.output(DAC_CLK,1)
    GPIO.output(DAC_CLK,0)   # Output RNG
    
    # 写入数据，一共8位
    i=8
    while i>0:
        num=num%256
        this_bit=int(num/128)
        GPIO.output(DAC_DATA,this_bit)
        GPIO.output(DAC_CLK,1)
        GPIO.output(DAC_CLK,0)   # Output Di
        num=num<<1
        i=i-1
    # 依据协议，一旦8位数据位都送入，LOAD变为低脉冲电平
    # 当LDAC为低电平时，在LOAD信号下降沿，将输入的数据锁入输出门，并立即产生模拟电压输出。
    GPIO.output(DAC_LOAD,0)
    
def loop(): # 循环
    while 1:
        num=int(input("input a integer(0~255):"))
        SendOneData(num)
        
if __name__ == '__main__': # 非库使用时程序入口
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
