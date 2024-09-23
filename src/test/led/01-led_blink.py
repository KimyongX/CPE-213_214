from machine import Pin
from time import sleep

red_led = Pin(4,Pin.OUT)
green_led = Pin(2,Pin.OUT)
blue_led = Pin(15,Pin.OUT)

red_led.value(0)
green_led.value(0)
blue_led.value(0)

while True:
    red_led.value(1)
    green_led.value(1)
    blue_led.value(1)
    sleep(1)
    red_led.value(0)
    green_led.value(0)
    blue_led.value(0)
    sleep(1)
    
