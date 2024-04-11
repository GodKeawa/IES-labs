#!/usr/bin/env python
#
#       This is a program for all ADC Module. It 
#   convert analog singnal to digital signal.
#
#       This program is most analog signal modules' 
#   dependency. Use it like this:
#       `import ADC0832`
#       `sig = ADC0832.getResult(chn)`
#
#   *'chn' should be 0 or 1 represent for ch0 or ch1
#   on ADC0832
#       
#         ACD1302                 Pi
#           CS ---------------- Pin 11
#           CLK --------------- Pin 12
#           DI ---------------- Pin 13

#           VCC ----------------- 3.3V
#           GND ------------------ GND
#

# 库引入
# RPi.GPIO库用于树莓派GPIO控制，wiringpi库也是用于GPIO控制，time库用于时间相关功能
import RPi.GPIO as GPIO 
import wiringpi
import time

# 定义ADC模块的引脚
ADC_CS  = 17 #11
ADC_CLK = 18 #12
ADC_DIO = 27 #13
usdelay = 2 # 最大时钟频率为400KHz，这里设置为2*2us
T_convert = 8*2*usdelay # ADC转换时间

# 使用默认引脚以保持向后兼容性
def setup(cs=17,clk=18,dio=27): #11,12,13
    global ADC_CS, ADC_CLK, ADC_DIO
    ADC_CS=cs
    ADC_CLK=clk
    ADC_DIO=dio
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)          # 以BCM编号引脚
    GPIO.setup(ADC_CS, GPIO.OUT)        # 将引脚设为输出
    GPIO.setup(ADC_CLK, GPIO.OUT)       # 将引脚设为输出

def destroy(): # 清理GPIO设置
    GPIO.cleanup()

# 使用通道0作为默认通道以保持向后兼容性
def getResult(channel=0):                   # 获取ADC结果，选择输入通道
    GPIO.setup(ADC_DIO, GPIO.OUT)  # 将DIO引脚设为输出
    
    GPIO.output(ADC_CS, 0)  # 使能片选信号，低电平表明开始工作
    
# 下面便是根据ADC0832的工作协议进行通道选择
    # 输入第一个时钟脉冲下降沿，并向DIO输出高电平，表示启始信号
    GPIO.output(ADC_CLK, 0)
    GPIO.output(ADC_DIO, 1);  wiringpi.delayMicroseconds(usdelay)
    # 重新拉高时钟脉冲
    GPIO.output(ADC_CLK, 1);  wiringpi.delayMicroseconds(usdelay)

    # 在第2、3个时钟脉冲下降沿向DIO输出一个高电平和一个channel
    # 依照协议，当channel为0时，便是CH0单端输入，channel为1时，便是CH1单端输入
    GPIO.output(ADC_CLK, 0)
    GPIO.output(ADC_DIO, 1);  wiringpi.delayMicroseconds(usdelay)

    GPIO.output(ADC_CLK, 1);  wiringpi.delayMicroseconds(usdelay)

    GPIO.output(ADC_CLK, 0)
    GPIO.output(ADC_DIO, channel);  wiringpi.delayMicroseconds(usdelay)

    GPIO.output(ADC_CLK, 1);  wiringpi.delayMicroseconds(usdelay)

# 第3个脉冲下降沿之后，输出DO进行转换数据的读取
# 我们这里将DIO设置为输入，并开始等待设置的T_convert时间让ADC0832进行处理
    GPIO.output(ADC_CLK, 0)
    GPIO.setup(ADC_DIO, GPIO.IN);  wiringpi.delayMicroseconds(T_convert)

# 根据工作协议，DIO将进行两次输出，我们将分别记录下来
# 第一次是从高位DATA7开始输出，第二次是从低位DATA0开始输出，所以处理方式不同
# 这里设置dat1和dat2是为了保证数据正确
    dat1 = 0 # 初始化为0
    for i in range(0, 8): # 循环输入时钟脉冲并读取数据，进行数据处理
        GPIO.output(ADC_CLK, 1);  wiringpi.delayMicroseconds(usdelay)
        GPIO.output(ADC_CLK, 0);  wiringpi.delayMicroseconds(usdelay)        
        dat1 = dat1 << 1 | GPIO.input(ADC_DIO) # 左移dat1

    # 都是下降沿读取数据
    dat2 = 0
    for i in range(0, 8):
        dat2 = dat2 | GPIO.input(ADC_DIO) << i # 左移DIO输出
        GPIO.output(ADC_CLK, 1);  wiringpi.delayMicroseconds(usdelay)
        GPIO.output(ADC_CLK, 0);  wiringpi.delayMicroseconds(usdelay)

# 这里在一个时钟脉冲里将CS设为高电平，使ADC0832停止工作
    GPIO.output(ADC_CLK, 1) 
    GPIO.output(ADC_CS, 1);  wiringpi.delayMicroseconds(usdelay)
    GPIO.output(ADC_CLK, 0);  wiringpi.delayMicroseconds(usdelay)

    if dat1 == dat2: # 比较两次读取的数据，确保数据正确
        return dat1
    else:
        return 0

def loop(): # 循环读取，两个模式都进行
    while True:
        res0 = getResult(0)
        res1 = getResult(1)
        print ('res0 = %d, res1 = %d' % (res0,res1))
        time.sleep(0.4)

# 当本文件是主文件时运行的内容，但本质上不会运行，本文件当作库使用
if __name__ == '__main__':      
    setup()
    try:
        loop()
    except KeyboardInterrupt:   
        destroy()