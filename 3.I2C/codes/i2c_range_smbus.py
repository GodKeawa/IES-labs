'''ultrasonic ranging using I2C'''
'''software tools : smbus'''
'''hardware       : KS103    '''

import smbus
import time

bus = smbus.SMBus(1) #open /dev/i2c-1
address = 0x74 #i2c device address(KS103的地址)
wr_cmd = 0xb0  #range 0-5m, return distance(mm) (写入参数)
#rd_cmd = 0xb2 
##range 0-5m, return flight time(us), remember divided by 2
try:
    while True:
        bus.write_byte_data(address, 0x2, wr_cmd) #发出探测指令
        time.sleep(1) #MIN ~ 0.033 等待探测数据
        HighByte = bus.read_byte_data(address, 0x2) #读取距离值
        LowByte = bus.read_byte_data(address, 0x3)
		Dist = (HighByte << 8) + LowByte #16位二进制数还原
        print('Distance:', Dist/10.0, 'cm')
        #time.sleep(2)
except KeyboardInterrupt:
    pass
bus.close()
print('Range over!')