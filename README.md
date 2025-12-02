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
As the last and main functionality of the software we have the main loop which is responsible of the monitorizing of our system. This every time the loop starts it will ask the needed informatio to the sensors and then that it will be written in the external and internal memory as csv. This type of format later will be come handy to be exported to excel for further analysis.
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

### Technical documentation


### Pitch Poster



https://github.com/micropython/micropython-lib/blob/master/LICENSE


