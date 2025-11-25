import time
import os
from machine import I2C, Pin
import dht12
import network
import ntptime
import problems
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
    #spi = machine.SPI(1,
    #baudrate=1000000,
    #polarity=0,
    #phase=0,
    #sck=machine.Pin(18),
    #mosi=machine.Pin(23),
    #miso=machine.Pin(19)
    #)
    #chip select
    #cs = machine.Pin(5, machine.Pin.OUT)
    
    #Initialize
    #sd = machine.SDCard(spi=spi, cs=cs)
    
    #Create sd
    #os.mount(sd, "/sd")
    
    #I2C Setup
    i2c =I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
    sensorTemHum = dht12.DHT12(i2c)

    led=Pin(2 , Pin.OUT)
    sensorconnection=0
    bugs = problems.ERRORS(i2c)
    while sensorconnection==0:
        sensorconnection= bugs.i2c_check()
        if sensorconnection==0:
            print("waiting for connection")
            for _ in range(5):
                led.off()
                time.sleep(0.5)
                led.on()
                time.sleep(0.5)
            
    # Function connect wifi get time
    def do_connect():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('conectando a la red')
            wlan.connect(SSID, PASSWORD)
            while not wlan.isconnected():
                time.sleep(1)
        print('configuración de red:', wlan.ifconfig())
        

    do_connect()
    
    try:
            ntptime.settime()
    except OSError:
        print("No se pudo conectar al servidor NTP. Verifique la conexión a internet.")
        
    #Prepare Altimeter to read
    
    i2c.writeto_mem(ADDR, PT_DATA_CFG, b'\x07') # Interruption activation
    i2c.writeto_mem(ADDR, CTRL_REG1, b'\x38')  # Standby
    i2c.writeto_mem(ADDR, CTRL_REG1, b'\x39')  # Active
    time.sleep(1)

    
    #Prepare storage
    with open("monitoreo.csv", "a") as storage:
 
        # Monitorize
        while True:
            
            #DHT12 section
            
            sensorTemHum.measure()
            t=sensorTemHum.temperature()
            h=sensorTemHum.humidity()
            
            #mpl3115a2 Section
            
            pressure_pa=0
            status = i2c.readfrom_mem(ADDR, STATUS, 1)
            if status[0] & 0x08:
                data = i2c.readfrom_mem(ADDR, OUT_P_MSB, 3)
                pres_raw = (data[0] << 16 | data[1] << 8 | data[2]) >> 6
                pressure_pa = pres_raw / 4.0
            else:
                print("error altimeter")
                
                
            local_time = time.localtime()
                
            print(f"Temperature: {t} C, Humidity: {h} RH, Relative Pressure: {pressure_pa:.2f} Pa, Year:{local_time[0]} , Month:{local_time[1]} , Day:{local_time[2]} , Hour:{local_time[3]}, Minute:{local_time[4]}, Second:{local_time[5]}" )
            time.sleep(1)
            
            
        #Export data
            storage.write(f"{t} C,{h} RH, {pressure_pa:.2f} Pa, {local_time[0]} {local_time[1]} {local_time[2]} {local_time[3]}:{local_time[4]}:{local_time[5]}\n")
            storage.flush() 
            #open("/sd/monitoring.csv","a").write(f"{t} C,{h} RH, {pressure_pa:.2f} Pa, {local_time[0]} {local_time[1]} {local_time[2]} {local_time[3]}:{local_time[4]}:{local_time[5]}\n")
            #open("/sd/monitoring.csv","a").flush()
        
        
        
        
except KeyboardInterrupt:
    
    print(f"Program stopped manually")
