# Import Library
from ssd1306 import SSD1306_I2C
from machine import Pin,SoftI2C
from time import sleep
from network import STA_IF,WLAN
import logging
from arduino_iot_cloud import ArduinoCloudClient

# Import Credential
from secrets import WIFI_SSID
from secrets import WIFI_PASSWORD
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD

# Pin Setup
oled_Pin = SoftI2C(scl=Pin(22),sda=Pin(21))

# Screen Resolution 
oled_ScreenWidth = 128
oled_ScreenHeight = 64

# OLED Interface 
oled = SSD1306_I2C(oled_ScreenWidth,oled_ScreenHeight,oled_Pin)

def wifi_connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASSWORD)
    while not wlan.isconnected():
        logging.info("Trying to connect to WIFI, Note this may take a while")
        sleep(0.5)
    logging.info("WIFI Connected")
    
def onMessageChange(client,value):
    print('Message from Arduino Cloud:{}'.format(value))
    oled.fill(0)
    oled.text(str(value),0,0)
    oled.show()
    
    if value == "Hello":
        client["message"] = "Hello from ESP32"
    
if __name__ == "__main__":
    logging.basicConfig(datefmt="%H:%M:%S",format="%(asctime)s.%(msecs)03d %(message)s",level=logging.INFO)
    
    wifi_connect()
    
    arduino_client = ArduinoCloudClient(device_id = DEVICE_ID,username=DEVICE_ID, password=CLOUD_PASSWORD)
    arduino_client.register('message',value=None,on_write=onMessageChange,interval=0.250)
    arduino_client.start()
