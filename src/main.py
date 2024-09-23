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

#---Function---
def set_angle(device,angle):
    while angle<0:
        angle+=180
    while angle>180:
        angle -= 180
    
    duty = int(500_000 + angle * 2_000_000/180)
    device.duty_ns(duty)

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

ultrasonic1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
ultrasonic2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)

oled_Pin = SoftI2C(scl=Pin(22),sda=Pin(21))
oled_ScreenWidth = 128
oled_ScreenHeight = 64
oled = SSD1306_I2C(oled_ScreenWidth,oled_ScreenHeight,oled_Pin)
