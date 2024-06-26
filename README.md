# Know Your Crop
An IOT Based Crop Prediction System

# Description

- IoT  
- Python-Django  
- Machine Learning - Random Forest Algorithm (Accuracy 99%)  
- Arduino IDE
- Thingspeak Server (Cloud Server For IoT Projects)  
- Dataset from Kaggle

# Hardware Used

- ESP8266 Node MCU  
- Arduino UNO Board  
- DHT11 Temperature and Humidity Sensor  
- Soil Moisture Sensor  
- Soil pH Sensor  
- Bread Board  
- Jumper Cables  

# Working  

The IoT-based Crop Prediction System using soil moisture, pH value, temperature, and 
humidity sensors aims to revolutionize modern agriculture by addressing key objectives. 
Firstly, the project seeks to establish a robust framework for real-time environmental 
monitoring, employing advanced sensors to continuously track crucial parameters like soil 
moisture, temperature, humidity, and pH Value. The sensors like DHT11, Soil moisture sensor, 
Soil pH Sensor  are used to collect the data with the help of ESP8266 NodeMCU and arduino 
UNO microcontrollers. These values that are sensed are then sent to Thingspeak cloud server 
from where these data are fetched by the webpage. Thingspeak Server is used  to visualize 
the data and notice the frequent changes in the data. The data that is fetched is produced to the 
trained Random Forest model with accuracy 99% for predicting the crop that is suitable for the 
given conditions.

# How to Run

- pip install requirements.txt
- cd kyc
- py manage.py runserver  

In the arduinuo ;
- Do the connections 
- Install IDE
- connect the devices and select the appropriate ports
- upload the code and program both devices


# Result Analysis 

![Connection](/Output_Images/connection.jpg)

![Prediction](/Output_Images/prediction.png)

![Thingspeak](/Output_Images/thingspeak.png)




