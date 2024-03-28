import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(0,2*np.pi,256) #linspace方法生成区间内等距点的坐标列表
S = np.sin(X) # 直接调用numpy里的方法就行
C = np.cos(X)

plt.title("matplotlib demo") # 设置标题
plt.xlim(-0.5,7)    # 设计x轴
plt.xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi],[0,r'$\pi/2$',r'$\pi$',r'$3*\pi/2$',r'$2*\pi$'])

plt.plot(X,S,label="Sin")   # 画Sin曲线 
plt.plot(X,C,label="Cos")   # 画Cos曲线
plt.legend(loc="lower left")    # 设置一个legend

plt.show()  # show