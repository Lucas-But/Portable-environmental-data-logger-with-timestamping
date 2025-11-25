import time
import machine

class Errors:
  def _init_(self, i2c):
    self.i2c=i2c

  def I2C_Check(self):
    adrrs= i2c.scan()
    if (adrrs[1]= 0x5c && adrrs[0]=0x60) || (adrrs[1]= 0x60 && adrrs[0]=0x5c):
      print("All the sensors are connected")
      return 1
    else:
      print("Problem Sensors. CHECK CONNECTION")
      return 0
      
