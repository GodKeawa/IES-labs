# 用到前面的信号采样函数和AD转换模块ADC0832，实现对信号的频谱分析。
import ADC0832
import time
import numpy as np
import matplotlib.pyplot as plt

def init():
    ADC0832.setup()
    
def loop():
# 取256点数据做FFT（快速傅立叶变换，离散傅里叶变换的一种高效算法，数据长度为2的幂时效果最佳）
# 实测得采样频率大约是3.7kHz。
    fft_size=256       # 256-point FFT
    # sampl_freq=5350  # 采样频率
    n=0
    y=[]
    t=time.time()
    while n<fft_size:
        digitalVal=ADC0832.getResult()
        n=n+1
        y.append(3.3*float(digitalVal)/255)
    t=time.time()-t
    sampl_freq = fft_size/t # 直接计算真实采样频率

    # 此函数对有限长实信号做快速傅立叶变换，得到fft_size/2+1个复数
    # 其中y_fft[0]是直流分量，y_fft[1]到y_fft[fft_size/2]是正频率分量
    # 实信号的负频率分量是正频率分量的共轭复数，不必单独列出
    y_fft=np.fft.rfft(y)    # Real signal（实信号）, Energy Scaled FFT（能量缩放FFT）

    y_fft_ampl=np.abs(y_fft)    # 只绘制幅度谱

    x=np.linspace(0,t,fft_size) # 用256均分时间，获取x轴坐标
    freq=np.linspace(0,sampl_freq/2,int(fft_size/2+1)) # 计算频谱上每一点的真实频率
    # 绘图，指定大小
    plt.figure(figsize=(8,4))
    # 两个子图，分别绘制时域波形和频域波形
    plt.subplot(211)
    plt.plot(x,y)
    plt.xlabel(u"t(s)")
    plt.title(u"Time domain")

    plt.subplot(212)
    plt.plot(freq,y_fft_ampl)
    plt.xlabel(u"freq(Hz)")
    plt.title(u"Frequency domain")
    # 调整子图之间的间距，展示图像
    plt.subplots_adjust(hspace=0.4)
    plt.show()

if __name__=='__main__':
    init()
    loop()
    ADC0832.destroy()
    print("The end!")