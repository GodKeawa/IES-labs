import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 21  # led由GPIO21控制
bt = 20  # button状态由GPIO20读取
GPIO.setup(led, GPIO.OUT)  # GPIO21设置为输出模式
GPIO.setup(bt, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO20设置为读入模式
ledStatus = False
n = 1
try:  # 提供退出方法，键盘输入Ctrl+c即可终止循环
    while True:
        time.sleep(0.01)
        if GPIO.input(bt) == GPIO.LOW:  # 读取到按键按下
            time.sleep(0.03)  # 睡0.03秒
            if GPIO.input(bt) == GPIO.HIGH:  # 如果此时读取到按键恢复
                print("button pressed", n)  # 输出语句
                n = n + 1
                ledStatus = not ledStatus  # 逆转ledStatus
                if ledStatus:  # 根据ledStatus设置GPIO21的输出电平，控制led亮灭
                    GPIO.output(led, GPIO.HIGH)
                else:
                    GPIO.output(led, GPIO.LOW)
except KeyboardInterrupt:
    pass
GPIO.cleanup()  # 清除setup的配置
