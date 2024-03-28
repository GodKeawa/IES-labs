# 1kg重的弹性小球高处坠落，已知初始高度为100m，初速度为0m/s
# 重力加速度为10m/s^2,风阻系数为r=0.1,且小球碰撞地面后以原速反弹（完全弹性碰撞）
# 利用python求解出小球在总世界20s内，高度随时间变化的轨迹

#设置向上为正方向，速度设为矢量，此时的加速度计算公式
# a = -g - v*r/m

import numpy as np
import matplotlib.pyplot as plt

m = 1       #质量为1kg
g = 10      #重力加速度为10m/s^2
r = 0.1     #风阻系数

v = [0]             #初速度列表
h = [100]          #高度列表
t = [0]             #时间列表
n = 1000       #可调整迭代次数
dt = 20.0 / n     #计算dt

#差分法
#h[n+1] = h[n] + v * dt
#v[n+1] = v[n] + a * dt

for i in range(n):  #本质上就是根据第i个数据把第i+1个数据append进去
    if (h[i] < 0 and v[i] < 0):  #检查高度，如果小于0了就让速度反向
        v[i] = -v[i]
    a = -g - v[i] * r / m   #即时计算加速度
    v.append(v[i] + a * dt)     #计算各个数据并append
    h.append(h[i] + v[i] * dt)  
    t.append(t[i] + dt)

#也可以尝试直接解析
#dv/dt = -g - v*r/m -> -dt = dv/(g+v*r/m) -> -t = ln(g+v*r/m)/(r/m)+C
#g+v*r/m = e^-((t+C)r/m) -> 10 + 0.1v = e^-0.1(t+C) -> v = 10*e^-0.1(t+C) - 100
#代入初始值t=0,v=0得到C=-lng/(r/m) -> -t = ln(1+v*r/(m*g))/(r/m) -> 1 + v*r/(m*g) = e^-(t*r/m)
#v = m*g/r(e^-(t*r/m)-1) = 100(e^(-0.1*t)-1) = 100*e^(-0.1*t)-100
#h = -e(-0.1*t)*1000 - 100t + C
#代入初值t=0,h=100,得到C = 1100 -> h = -1000*e(-0.1*t) - 100t + 1100
#考虑反弹，第一个方程将运行到h = 0,之后v反弹，需要先重设速度方程的常数C，再重设h的方程常数C
#由v = 10*e^-0.1(t+C) - 100 再积分，得到h = -100*e^-0.1(t+C1) - 100t + C2
    
Cv = -np.log(10) * 10   #初始速度方程常量
Ch = 1100   #初始高度方程常量

def tTov(t,v,flag): #速度方程抽象为一个函数，且根据flag动态调整global的常量Cv
    global Cv
    if flag:
        Cv = -t - np.log(10 + v*0.1) * 10
    return (10*np.e ** (-0.1*(t+Cv)) - 100)

def tToh(t,h,flag): #高度方程同样抽象，并更新常量Ch
    global Cv,Ch
    if flag:
        Ch = h + 100*t + 100*np.e ** (-0.1*(t+Cv))
    return (Ch - 100*t - 100*np.e ** (-0.1*(t+Cv)))

flag = 0    #flag表征是否落地
T = t   #时间表复制一份差分法的，这样坐标系可以对准
H = [100]   #高度列表
V = [0]     #速度列表
for i in range(n):  #本质上是根据解析方程代入每个t计算，但是因为有常量更新，所以终归还是要循环
    if (H[i] < 0 and V[i] < 0): #检查是否落地
        V[i] = -V[i] #依旧速度反向
        flag = 1    #设置flag
    V.append(tTov(T[i],V[i],flag))  #这里顺序很重要，必须先更新Cv才能去更新Ch
    H.append(tToh(T[i],H[i],flag))
    flag = 0    #重设flag
    

#创建图像
def init(): #设计一个初始化函数
    plt.xlabel("time:",loc="left") #轴名称和位置设置一下
    plt.ylabel("height:",loc="bottom")
    ax = plt.gca()
    ax.xaxis.set_ticks([]) #删除原本的坐标线
    ax.yaxis.set_ticks([])
    x = np.linspace(0,20,21) #x轴设计一下
    plt.xticks(x)
    y = np.linspace(0,100,11) #y轴设计一下
    plt.yticks(y)
    
plt.figure(figsize=(16,8),dpi=80)   #让整个画面舒服一点
plt.title("falling ball simulating") #设置一个大标题
ax = plt.gca()
ax.xaxis.set_ticks([]) #删除figure的坐标线
ax.yaxis.set_ticks([])
ax.spines["top"].set_color(None) #删除figure无用的线
ax.spines["bottom"].set_color(None)

plt.subplot(1,2,1) #开一下subplot
init()
plt.title("difference methods") #差分法
plt.plot(t,h)

plt.subplot(1,2,2)
init()
plt.title("analytic method") #解析法
plt.plot(T,H)

plt.show()  #show


