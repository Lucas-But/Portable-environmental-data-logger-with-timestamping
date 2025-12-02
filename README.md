<img width="4621" height="4621" alt="image" src="https://github.com/user-attachments/assets/605c0df4-116f-4b21-9aa7-e31e895c3f33" />



# Portable-environmental-data-logger-with-timestamping
## Project development
Nowadays all the renowable energy sources are dependant of the enviroment and its changes. Due to this fact before installing this type of big energy production plants, a enviromental study shoud be done to ensure the area it is suitable. In order to do the research we propose to use a **ESP32** to collect and store environmental **data** (temperature, pressure, light, motion, etc.) to an **SD card** or **internal memory**. Include a real-time clock for **timestamping**. **Export** data to computer to further analysis.


Our goal with this project is to create an autonomous weather station that colects enviromental data, such as: temperature, preassure and humidity. To fulfil this function we will be using some sensors connected via serial communication to the MCU that will collect, process and store it in order to use it after. All this processes will be continiously monitorized by the MCU and each value will be timestamped to the moment when it was measured.


### Table-with-used-components
 
| ***Components***               | ***Description*** | ***Image*** |
|-------------------------|-------------|--------|
| **DHT12**               | Sensor for temperature and humidity | <img width="280" src="https://github.com/user-attachments/assets/febfc58d-2e2b-428f-95a7-ecf16ace6886" /> |
| **MPL3115A2**           | Sensor for preasure | <img width="320"  src="https://github.com/user-attachments/assets/046d3865-2a43-4418-84c7-81b585e957b8" /> |
| **MicroSD Module**      | Module to conect the SD card to the ESP32 | <img width="320"  src="https://github.com/user-attachments/assets/16de2077-ac19-4f89-b3d6-b01bca7977c4" /> |
| **ESP32 FireBeetle**    | Microprocesor | <img width="320"  src="https://github.com/user-attachments/assets/b03e0de9-60dd-40b8-ad49-f7ffebcfeb84" /> |
| **MicroSD 8GB**    | SD storage | <img width="320" height="543" alt="image" src="https://github.com/user-attachments/assets/2ddc0fa7-6497-4d66-8750-d3dac361974c" />|

https://github.com/mcauser/micropython-dht12/tree/master

### Software Logic
With the following flow chart we describes the main process of our sofware:


<img width="2105" height="5747" alt="image" src="https://github.com/user-attachments/assets/a99b40f2-1897-4b87-a10f-c3d1e3342a34" />

## Project Development
### Project Demonstration


### Documented Code
The code it is divided in two main types the ones developed in by ourselfs and the ones that have been imported to use it as libraries.
#### Own code
##### Main
In the main we can find 7 stages of the code:
###### 1st stage: Initialization
In the first phase of the main our program initialize all the constants and communication protocols as well as create the memory space of the sd card:
```python
try:
#Constants
    ADDR = 0x60
    CTRL_REG1 = 0x26
    PT_DATA_CFG = 0x13
    STATUS = 0x00
    OUT_P_MSB = 0x01
    SSID="UREL-SC661-V-2.4G"
    PASSWORD="TomFryza"
    
    #SPI setup card
    spi = machine.SPI(1,
    baudrate=100000,
    polarity=0,
    phase=0,
    sck=machine.Pin(18),
    mosi=machine.Pin(23),
    miso=machine.Pin(19)
    )
    #chip select
    cs = machine.Pin(5, machine.Pin.OUT)
    
    #Initialize
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    
    #I2C Setup
    i2c =I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
    sensorTemHum = dht12.DHT12(i2c)

    led1=Pin(2 , Pin.OUT)
    led2=Pin(26 , Pin.OUT)
    sensorconnection=0
    bugs = tools.ERRORS(i2c)
```
###### 2nd stage:Connection Verification
In this stage all the connections to the sensors are checked in order to ensure a proper function of our system.
```python
    sensorconnection=0
    bugs = tools.ERRORS(i2c)
    while sensorconnection==0:
        sensorconnection= bugs.i2c_check()
        if sensorconnection==0:
            print("waiting for connection")
            for _ in range(5):
                led1.off()
                time.sleep(0.5)
                led1.on()
                time.sleep(0.5)

```

###### 3rd stage:Network & Time Sync
In this part we use a function from our custom library named tools to make a connection to the internet so we can get the time:
```python
 tools.do_connect()
    
    try:
            ntptime.settime()
    except OSError:
        print("Cannot synchronize time. CHECK INTERNET CONNECTION")
```
###### 4th stage:Sensor Configuration
In this phase we activate the interruption register from mpl3115a2 that messures the pressure, we put the sensor in standby and then we activate it. For stability reason we have implemented a time sleep so the sensor could be set properly.
```python
i2c.writeto_mem(ADDR, PT_DATA_CFG, b'\x07') # Interruption activation
    i2c.writeto_mem(ADDR, CTRL_REG1, b'\x38')  # Standby
    i2c.writeto_mem(ADDR, CTRL_REG1, b'\x39')  # Active
    time.sleep(1)
```

###### 5th stage:Storage Preparation
In this case we have prepared two types of storage so in order fails one we have the backup of the other one. So, it has been set up as "storageI" the internal storage of the ESP32 and the "StorageE" as an external SD card. Furthermore, we have set that the first time it is read a heading with each type of data and the time of the start will be recorded
```python
storageI = open("monitoring.csv", "a")
    storageE = open("/sd/monitoring.csv","a")
    local_time = time.localtime()
    storageE.write(f"temperature,humidity, Pressure, Time(started:{local_time[0]} {local_time[1]} {local_time[2]} {local_time[3]}:{local_time[4]}:{local_time[5]})\n")

```

###### 6th stage:Monitoring Loop
As the last and main functionality of the software we have the main loop which is responsible of the monitorizing of our system. This every time the loop starts it will ask the needed information to the sensors and then that it will be written in the external and internal memory as csv. This type of format later will be come handy to be exported to excel for further analysis.
```python
while True:
        led2.off()
        #DHT12 section
        
        sensorTemHum.measure()
        t=sensorTemHum.temperature()
        h=sensorTemHum.humidity()
        
        #mpl3115a2 Section
        
        pressure_pa=0
        status = i2c.readfrom_mem(ADDR, STATUS, 1)
        if status[0] & 0x08:
            data = i2c.readfrom_mem(ADDR, OUT_P_MSB, 3)
            pressure_pa = (data[0] << 16 | data[1] << 8 | data[2]) >> 6
        else:
            print("error altimeter")
            
            
        local_time = time.localtime()
            
        print(f"Temperature: {t} C, Humidity: {h} RH, Relative Pressure: {pressure_pa:.2f} Pa, Year:{local_time[0]} , Month:{local_time[1]} , Day:{local_time[2]} , Hour:{local_time[3]}, Minute:{local_time[4]}, Second:{local_time[5]}" )
        time.sleep(1)
        
        
    #Export data
        storageI.write(f"{t} C,{h} RH, {pressure_pa:.2f} Pa, {local_time[0]} {local_time[1]} {local_time[2]} {local_time[3]}:{local_time[4]}:{local_time[5]}\n")
        time.sleep(0.25)
        storageI.flush()
        
         
        storageE.write(f"{t} C,{h} RH, {pressure_pa:.2f} Pa, {local_time[0]} {local_time[1]} {local_time[2]} {local_time[3]}:{local_time[4]}:{local_time[5]}\n")
        time.sleep(0.25)
        storageE.flush()
        led2.on()
        time.sleep(0.25)
```

###### 7th stage:Manual Interruption 
As a final stage if a error would happen there is an exception to stop the programme and a message will showcase that it has been stopped manually
```python
except KeyboardInterrupt:
    
    print(f"Program stopped manually")
```
##### Tools
The tools library was created to gather all the support functions made for the main program and we can difference one class and one function.
###### Class Errors
This class was made in order to strengthen our code through some check ups that it will be made in order to ensure its correct status
````python
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

````
###### Def Connection
This function was made to connect the esp32 to internet and it was written in the tools so it could be used repeteadly through the program.
```python
 def do_connect():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
            if not wlan.isconnected():
                print('connecting to the network')
                wlan.connect(SSID, PASSWORD)
                while not wlan.isconnected():
                    time.sleep(1)
                print('network configuration:', wlan.ifconfig())
```
#### Code downloaded from other githubs
##### dht12 libraries
This were downloaded from a github https://github.com/mcauser/micropython-dht12/tree/master the code it was located in the source carpet. This library contains some funcionalities for our sensor and has a MIT license so we are granted with permission to use it.
```python
# SPDX-FileCopyrightText: 2016 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython Aosong DHT12 I2C driver
https://github.com/mcauser/micropython-dht12
"""

from micropython import const

__version__ = "1.1.0"

I2C_ADDRESS = const(0x5C)  # fixed I2C address


class DHT12:
    def __init__(self, i2c):
        self._i2c = i2c
        self._buf = bytearray(5)

    def check(self):
        if self._i2c.scan().count(I2C_ADDRESS) == 0:
            raise OSError(f"DHT12 not found at I2C address {I2C_ADDRESS:#x}")
        return True

    def measure(self):
        buf = self._buf
        self._i2c.readfrom_mem_into(I2C_ADDRESS, 0, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xFF != buf[4]:
            raise ValueError("Checksum error")

    def temperature(self):
        t = self._buf[2] + (self._buf[3] & 0x7F) * 0.1
        if self._buf[3] & 0x80:
            t = -t
        return t

    def humidity(self):
        return self._buf[0] + self._buf[1] * 0.1
```
##### sdcard library
This library is has a class that is in charge of creating the connection between the ESP32 and the sd card module via SPI. The code was substarcted from this webpage: https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard and the repository is with an MIT license that allows us to use it.
<details>
<summary> View code from library </summary>
```python
 
#MicroPython driver for SD cards using SPI bus.

#Requires an SPI bus and a CS pin.  Provides readblocks and writeblocks
#methods so the device can be mounted as a filesystem.

#Example usage on pyboard:

    #import pyb, sdcard, os
    #sd = sdcard.SDCard(pyb.SPI(1), pyb.Pin.board.X5)
    #pyb.mount(sd, '/sd2')
    #os.listdir('/')

#Example usage on ESP8266:

    #import machine, sdcard, os
    #sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))
    #os.mount(sd, '/sd')
    #os.listdir('/')



from micropython import const
import time


_CMD_TIMEOUT = const(100)

_R1_IDLE_STATE = const(1 << 0)
#R1_ERASE_RESET = const(1 << 1)
_R1_ILLEGAL_COMMAND = const(1 << 2)
#R1_COM_CRC_ERROR = const(1 << 3)
#R1_ERASE_SEQUENCE_ERROR = const(1 << 4)
#R1_ADDRESS_ERROR = const(1 << 5)
#R1_PARAMETER_ERROR = const(1 << 6)
_TOKEN_CMD25 = const(0xFC)
_TOKEN_STOP_TRAN = const(0xFD)
_TOKEN_DATA = const(0xFE)


class SDCard:
    def __init__(self, spi, cs, baudrate=1320000):
        self.spi = spi
        self.cs = cs

        self.cmdbuf = bytearray(6)
        self.dummybuf = bytearray(512)
        self.tokenbuf = bytearray(1)
        for i in range(512):
            self.dummybuf[i] = 0xFF
        self.dummybuf_memoryview = memoryview(self.dummybuf)

        # initialise the card
        self.init_card(baudrate)

    def init_spi(self, baudrate):
        try:
            master = self.spi.MASTER
        except AttributeError:
            # on ESP8266
            self.spi.init(baudrate=baudrate, phase=0, polarity=0)
        else:
            # on pyboard
            self.spi.init(master, baudrate=baudrate, phase=0, polarity=0)

    def init_card(self, baudrate):
        # init CS pin
        self.cs.init(self.cs.OUT, value=1)

        # init SPI bus; use low data rate for initialisation
        self.init_spi(100000)

        # clock card at least 100 cycles with cs high
        for i in range(16):
            self.spi.write(b"\xff")

        # CMD0: init card; should return _R1_IDLE_STATE (allow 5 attempts)
        for _ in range(5):
            if self.cmd(0, 0, 0x95) == _R1_IDLE_STATE:
                break
        else:
            raise OSError("no SD card")

        # CMD8: determine card version
        r = self.cmd(8, 0x01AA, 0x87, 4)
        if r == _R1_IDLE_STATE:
            self.init_card_v2()
        elif r == (_R1_IDLE_STATE | _R1_ILLEGAL_COMMAND):
            self.init_card_v1()
        else:
            raise OSError("couldn't determine SD card version")

        # get the number of sectors
        # CMD9: response R2 (R1 byte + 16-byte block read)
        if self.cmd(9, 0, 0, 0, False) != 0:
            raise OSError("no response from SD card")
        csd = bytearray(16)
        self.readinto(csd)
        if csd[0] & 0xC0 == 0x40:  # CSD version 2.0
            self.sectors = ((csd[7] << 16 | csd[8] << 8 | csd[9]) + 1) * 1024
        elif csd[0] & 0xC0 == 0x00:  # CSD version 1.0 (old, <=2GB)
            c_size = (csd[6] & 0b11) << 10 | csd[7] << 2 | csd[8] >> 6
            c_size_mult = (csd[9] & 0b11) << 1 | csd[10] >> 7
            read_bl_len = csd[5] & 0b1111
            capacity = (c_size + 1) * (2 ** (c_size_mult + 2)) * (2**read_bl_len)
            self.sectors = capacity // 512
        else:
            raise OSError("SD card CSD format not supported")
        # print('sectors', self.sectors)

        # CMD16: set block length to 512 bytes
        if self.cmd(16, 512, 0) != 0:
            raise OSError("can't set 512 block size")

        # set to high data rate now that it's initialised
        self.init_spi(baudrate)

    def init_card_v1(self):
        for i in range(_CMD_TIMEOUT):
            time.sleep_ms(50)
            self.cmd(55, 0, 0)
            if self.cmd(41, 0, 0) == 0:
                # SDSC card, uses byte addressing in read/write/erase commands
                self.cdv = 512
                # print("[SDCard] v1 card")
                return
        raise OSError("timeout waiting for v1 card")

    def init_card_v2(self):
        for i in range(_CMD_TIMEOUT):
            time.sleep_ms(50)
            self.cmd(58, 0, 0, 4)
            self.cmd(55, 0, 0)
            if self.cmd(41, 0x40000000, 0) == 0:
                self.cmd(58, 0, 0, -4)  # 4-byte response, negative means keep the first byte
                ocr = self.tokenbuf[0]  # get first byte of response, which is OCR
                if not ocr & 0x40:
                    # SDSC card, uses byte addressing in read/write/erase commands
                    self.cdv = 512
                else:
                    # SDHC/SDXC card, uses block addressing in read/write/erase commands
                    self.cdv = 1
                # print("[SDCard] v2 card")
                return
        raise OSError("timeout waiting for v2 card")

    def cmd(self, cmd, arg, crc, final=0, release=True, skip1=False):
        self.cs(0)

        # create and send the command
        buf = self.cmdbuf
        buf[0] = 0x40 | cmd
        buf[1] = arg >> 24
        buf[2] = arg >> 16
        buf[3] = arg >> 8
        buf[4] = arg
        buf[5] = crc
        self.spi.write(buf)

        if skip1:
            self.spi.readinto(self.tokenbuf, 0xFF)

        # wait for the response (response[7] == 0)
        for i in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            response = self.tokenbuf[0]
            if not (response & 0x80):
                # this could be a big-endian integer that we are getting here
                # if final<0 then store the first byte to tokenbuf and discard the rest
                if final < 0:
                    self.spi.readinto(self.tokenbuf, 0xFF)
                    final = -1 - final
                for j in range(final):
                    self.spi.write(b"\xff")
                if release:
                    self.cs(1)
                    self.spi.write(b"\xff")
                return response

        # timeout
        self.cs(1)
        self.spi.write(b"\xff")
        return -1

    def readinto(self, buf):
        self.cs(0)

        # read until start byte (0xff)
        for i in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] == _TOKEN_DATA:
                break
            time.sleep_ms(1)
        else:
            self.cs(1)
            raise OSError("timeout waiting for response")

        # read data
        mv = self.dummybuf_memoryview
        if len(buf) != len(mv):
            mv = mv[: len(buf)]
        self.spi.write_readinto(mv, buf)

        # read checksum
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")

        self.cs(1)
        self.spi.write(b"\xff")

    def write(self, token, buf):
        self.cs(0)

        # send: start of block, data, checksum
        self.spi.read(1, token)
        self.spi.write(buf)
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")

        # check the response
        if (self.spi.read(1, 0xFF)[0] & 0x1F) != 0x05:
            self.cs(1)
            self.spi.write(b"\xff")
            return

        # wait for write to finish
        while self.spi.read(1, 0xFF)[0] == 0:
            pass

        self.cs(1)
        self.spi.write(b"\xff")

    def write_token(self, token):
        self.cs(0)
        self.spi.read(1, token)
        self.spi.write(b"\xff")
        # wait for write to finish
        while self.spi.read(1, 0xFF)[0] == 0x00:
            pass

        self.cs(1)
        self.spi.write(b"\xff")

    def readblocks(self, block_num, buf):
        # workaround for shared bus, required for (at least) some Kingston
        # devices, ensure MOSI is high before starting transaction
        self.spi.write(b"\xff")

        nblocks = len(buf) // 512
        assert nblocks and not len(buf) % 512, "Buffer length is invalid"
        if nblocks == 1:
            # CMD17: set read address for single block
            if self.cmd(17, block_num * self.cdv, 0, release=False) != 0:
                # release the card
                self.cs(1)
                raise OSError(5)  # EIO
            # receive the data and release card
            self.readinto(buf)
        else:
            # CMD18: set read address for multiple blocks
            if self.cmd(18, block_num * self.cdv, 0, release=False) != 0:
                # release the card
                self.cs(1)
                raise OSError(5)  # EIO
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                # receive the data and release card
                self.readinto(mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            if self.cmd(12, 0, 0xFF, skip1=True):
                raise OSError(5)  # EIO

    def writeblocks(self, block_num, buf):
        # workaround for shared bus, required for (at least) some Kingston
        # devices, ensure MOSI is high before starting transaction
        self.spi.write(b"\xff")

        nblocks, err = divmod(len(buf), 512)
        assert nblocks and not err, "Buffer length is invalid"
        if nblocks == 1:
            # CMD24: set write address for single block
            if self.cmd(24, block_num * self.cdv, 0) != 0:
                raise OSError(5)  # EIO

            # send the data
            self.write(_TOKEN_DATA, buf)
        else:
            # CMD25: set write address for first block
            if self.cmd(25, block_num * self.cdv, 0) != 0:
                raise OSError(5)  # EIO
            # send the data
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.write(_TOKEN_CMD25, mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            self.write_token(_TOKEN_STOP_TRAN)

    def ioctl(self, op, arg):
        if op == 4:  # get number of blocks
            return self.sectors
        if op == 5:  # get block size in bytes
            return 512
```
</details>

### Technical documentation


### Pitch Poster



https://github.com/micropython/micropython-lib/blob/master/LICENSE


