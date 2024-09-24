#---Import Library---
from time import sleep
from ssd1306 import SSD1306_I2C
from machine import Pin,SoftI2C,PWM
from network import STA_IF,WLAN
import logging
from arduino_iot_cloud import ArduinoCloudClient
from hcsr04 import HCSR04
from servo import Servo

#---Import Credential---
from secrets import WIFI_SSID
from secrets import WIFI_PASSWORD
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD
from secrets import LINE_NOTIFY_TOKEN

#---Pin Setup---
red_led = Pin(4,Pin.OUT)
green_led = Pin(2,Pin.OUT)
blue_led = Pin(15,Pin.OUT)

buzzer = Pin(12,Pin.OUT)
beep = PWM(buzzer,500)
beep.duty(500)
sleep(0.1)
beep.deinit()

btn1_Pin = Pin(13,Pin.IN)

sensor1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)

oled_Pin = SoftI2C(scl=Pin(22),sda=Pin(21))
oled_ScreenWidth = 128
oled_ScreenHeight = 64
oled = SSD1306_I2C(oled_ScreenWidth,oled_ScreenHeight,oled_Pin)

#---Function---
def wifi_connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASSWORD)
    while not wlan.isconnected():
        logging.info("Trying to connect to WIFI, Note this may take a while")
        sleep(0.5)
    logging.info("WIFI Connected!")
    logging.info(f"{wlan.ifconfig()}")

def readDistance1(client):
    distance1 = sensor1.distance_cm()
    return distance1

def readDistance2(client):
    distance2 = sensor2.distance_cm()
    return distance2

def onMessageChange(client,value):
    print('Message from Arduino Cloud:{}'.format(value))

def onBuzzerChange(client,value):
    print('Buzzer value from Arduino Cloud: {}'.format(value))
    
    if value == True:
        beep = PWM(buzzer,1000)
        beep.duty(1000)
        sleep(1)
        beep.deinit()

def onServoStateChange(client,value):
    print('Servo value from Arduino Cloud: {}'.format(value))
        
if __name__ == "__main__":
    logging.basicConfig(datefmt="%H:%M:%S",format="%(asctime)s.%(msecs)03d %(message)s",level=logging.INFO)
    wifi_connect()
    
    arduino_client = ArduinoCloudClient(device_id = DEVICE_ID,username=DEVICE_ID, password=CLOUD_PASSWORD)
    arduino_client.register('message',value=None,on_write=onMessageChange,interval=0.250)
    arduino_client.register('distance1',value=None,on_read=readDistance1,interval=0.250)
    arduino_client.register('distance2',value=None,on_read=readDistance2,interval=0.250)
    arduino_client.register('buzzer_state',value=None,on_write=onBuzzerChange,interval=0.250)
    arduino_client.register('servo_state',value=None,on_write=onBuzzerChange,interval=0.250)
    arduino_client.start()
    
    while True:
        arduino_client.update()
