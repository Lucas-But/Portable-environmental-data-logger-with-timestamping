# Portable-environmental-data-logger-with-timestamping
Collect and store environmental **data** (temperature, pressure, light, motion, etc.) to an SD card or **internal memory**. Include a real-time clock for **timestamping**. **Export** data to computer.




Our goal with this project is to create an autonomous weather station that colects enviromental data, such as: temperature, preassure and humidity. To fulfil this function we will be using some sensors connected via serial communication to the MCU that will collect, process, and store or send it in order to use it after. All this processes will be continiously monitorized by the MCU and each value will be stored assigned to the moment when it was measured.


# Table-with-used-components
 
| ***Components***               | ***Description*** | ***Image*** |
|-------------------------|-------------|--------|
| **DHT12**               | Sensor for temperature and humidity | <img width="280" src="https://github.com/user-attachments/assets/febfc58d-2e2b-428f-95a7-ecf16ace6886" /> |
| **MPL3115A2**           | Sensor for preasure | <img width="320"  src="https://github.com/user-attachments/assets/046d3865-2a43-4418-84c7-81b585e957b8" /> |
| **MicroSD Module**      | Module to conect the SD card to the ESP32 | <img width="320"  src="https://github.com/user-attachments/assets/16de2077-ac19-4f89-b3d6-b01bca7977c4" /> |
| **ESP32 FireBeetle**    | Microprocesor | <img width="320"  src="https://github.com/user-attachments/assets/b03e0de9-60dd-40b8-ad49-f7ffebcfeb84" /> |
| **MicroSd 8GB**    | Microprocesor | <img width="320" height="543" alt="image" src="https://github.com/user-attachments/assets/2ddc0fa7-6497-4d66-8750-d3dac361974c" />
 |

https://github.com/mcauser/micropython-dht12/tree/master



https://github.com/micropython/micropython-lib/blob/master/LICENSE

Components we used to fulfil the project:
ESP32-firebeetle

DHT12 sensor

