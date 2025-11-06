# Portable-environmental-data-logger-with-timestamping
Collect and store environmental **data** (temperature, pressure, light, motion, etc.) to an SD card or **internal memory**. Include a real-time clock for **timestamping**. **Export** data to computer.

Our goal with this project is to create an autonomous station that colects enviromental data, such as: temperature, preassure and humidity. For fulfil this function we will be using some sensors connected via serial communication to the MCU that will colect, process, and store or send it in order to use it after. All this processes will be continiously monitorized by the MCU and each value will be stored assigned to the moment when it was measured.

To complete all this we will be using the following components: DHT12 for temperature and humidity, MPL3115A2 for pressure, RTC/DS3231 to know what time it is and ESP32 to process all this data and do the following steps.
