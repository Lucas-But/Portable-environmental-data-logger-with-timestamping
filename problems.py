import time
import machine

class ERRORS:
  def _init_(self, i2c):
    self.i2c=i2c

  def i2c_check(self):
    addrs= i2c.scan()
    if (hex(addrs[1])= 0x5c && hex(addrs[0])=0x60) || (hex(addrs[1])= 0x60 && hex(addrs[0]=0x5c)):
      print("All the sensors are connected")
      return 1
    else:
      print("Problem Sensors. CHECK CONNECTION")
      return 0
      
