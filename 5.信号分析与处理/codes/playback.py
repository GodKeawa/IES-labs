# 引入AD转换和DA转换的库
import ADC0832
import DAC_TLC5620 as DAC
import time
import numpy as np
import matplotlib.pyplot as plt

def init(): # 初始化
    ADC0832.setup()
    DAC.setup()
    
def loop(): # 循环
    while 1:
        digitalVal=ADC0832.getResult() # 从ADC0832获取结果
        # Call some functions for signal processing
        
        DAC.SendOneData(digitalVal) # 输出到DAC
        
if __name__=='__main__': # 非库使用时程序入口
    init()
    loop()
    ADC0832.destroy()
    DAC.destroy()
    print("The end!")