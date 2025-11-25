import time
import machine

class ERRORS:
  def __init__(self, i2c):
    self.i2c=i2c

  def i2c_check(self):
    addrs= self.i2c.scan()
    if (addrs[1]== 0x5c and addrs[0]==0x60) or (addrs[1]== 0x60 and addrs[0]==0x5c):
      print("All the sensors are connected")
      return 1
    else:
      print("Problem Sensors. CHECK CONNECTION")
      return 0
def do_connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to the network')
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
      time.sleep(1)
    print('network configuration:', wlan.ifconfig())
      
