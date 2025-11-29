<img width="4621" height="4621" alt="image" src="https://github.com/user-attachments/assets/605c0df4-116f-4b21-9aa7-e31e895c3f33" />



# Portable-environmental-data-logger-with-timestamping

Nowadays all the renowable energy sources are dependant of the enviroment and its changes. Due to this fact before installing this type of big energy production plants, a enviromental study shoud be done to ensure the aerea it is suitable. In order to do the research we propose to use a **ESP32** to collect and store environmental **data** (temperature, pressure, light, motion, etc.) to an **SD card** or **internal memory**. Include a real-time clock for **timestamping**. **Export** data to computer to further analysis.


Our goal with this project is to create an autonomous weather station that colects enviromental data, such as: temperature, preassure and humidity. To fulfil this function we will be using some sensors connected via serial communication to the MCU that will collect, process and store it in order to use it after. All this processes will be continiously monitorized by the MCU and each value will be timestamped to the moment when it was measured.


# Table-with-used-components
 
| ***Components***               | ***Description*** | ***Image*** |
|-------------------------|-------------|--------|
| **DHT12**               | Sensor for temperature and humidity | <img width="280" src="https://github.com/user-attachments/assets/febfc58d-2e2b-428f-95a7-ecf16ace6886" /> |
| **MPL3115A2**           | Sensor for preasure | <img width="320"  src="https://github.com/user-attachments/assets/046d3865-2a43-4418-84c7-81b585e957b8" /> |
| **MicroSD Module**      | Module to conect the SD card to the ESP32 | <img width="320"  src="https://github.com/user-attachments/assets/16de2077-ac19-4f89-b3d6-b01bca7977c4" /> |
| **ESP32 FireBeetle**    | Microprocesor | <img width="320"  src="https://github.com/user-attachments/assets/b03e0de9-60dd-40b8-ad49-f7ffebcfeb84" /> |
| **MicroSD 8GB**    | SD storage | <img width="320" height="543" alt="image" src="https://github.com/user-attachments/assets/2ddc0fa7-6497-4d66-8750-d3dac361974c" />|

https://github.com/mcauser/micropython-dht12/tree/master

# Software Logic
<img width="6820" height="5747" alt="image" src="https://github.com/user-attachments/assets/9efe02a5-ee58-49a4-ba2c-5420ef277649" />


https://github.com/micropython/micropython-lib/blob/master/LICENSE

Components we used to fulfil the project:
ESP32-firebeetle

DHT12 sensor

