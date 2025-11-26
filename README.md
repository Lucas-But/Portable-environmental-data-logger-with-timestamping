# Portable-environmental-data-logger-with-timestamping
Collect and store environmental **data** (temperature, pressure, light, motion, etc.) to an SD card or **internal memory**. Include a real-time clock for **timestamping**. **Export** data to computer.

Our goal with this project is to create an autonomous weather station that colects enviromental data, such as: temperature, preassure and humidity. To fulfil this function we will be using some sensors connected via serial communication to the MCU that will collect, process, and store or send it in order to use it after. All this processes will be continiously monitorized by the MCU and each value will be stored assigned to the moment when it was measured.

To complete all this we will be using the following components: 
 | - DHT12 --> for temperature and humidity | <img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/febfc58d-2e2b-428f-95a7-ecf16ace6886" /> |
 | - MPL3115A2 --> for pressure | <img width="1020" height="570" alt="image" src="https://github.com/user-attachments/assets/046d3865-2a43-4418-84c7-81b585e957b8" /> |
 | - "microSD card reader module --> to store the data measured. Aftewards to have the possibility to export that data." | <img width="1200" height="709" alt="image" src="https://github.com/user-attachments/assets/16de2077-ac19-4f89-b3d6-b01bca7977c4" /> |
 | - ESP32-firebeetle --> to process all this data and do the following steps. | <img width="871" height="710" alt="image" src="https://github.com/user-attachments/assets/b03e0de9-60dd-40b8-ad49-f7ffebcfeb84" /> |

https://github.com/mcauser/micropython-dht12/tree/master



https://github.com/micropython/micropython-lib/blob/master/LICENSE

Components we used to fulfil the project:
ESP32-firebeetle

DHT12 sensor

