"""ultrasonic ranging using I2C"""

"""software tools : pigpio"""
"""hardware       : KS103    """

import pigpio
import time

import pigpio
import time

pi = pigpio.pi()  # 创建一个daemon的实例pi
if not pi.connected:  # 查看是否连接成功
    exit()
address = 0x74  # i2c device address(k103地址)
h = pi.i2c_open(1, address)  # open device at address on bus 1，返回设备对象句柄
wr_cmd = 0xB0  # range 0-5m, return distance(mm)
# rd_cmd = 0xb2
##range 0-5m, return flight time(us), remember divided by 2
try:
    while True:  # 同上
        pi.i2c_write_byte_data(h, 0x2, wr_cmd)  # 通过设备对象句柄发出探测指令
        time.sleep(1)  # MIN ~ 0.033
        HighByte = pi.i2c_read_byte_data(h, 0x2)  # 通过设备对象句柄读取数据
        LowByte = pi.i2c_read_byte_data(h, 0x3)
        Dist = (HighByte << 8) + LowByte
        print("Distance:", Dist / 10.0, "cm")
        # time.sleep(2)
except KeyboardInterrupt:
    pass
pi.i2c_close(h)
print("Range over!")
