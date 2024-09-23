from machine import Pin
from time import sleep

btn1_Pin = Pin(13,Pin.IN)

while True:
    btn_state = btn1_Pin.value()
    
    if btn_state == 1:
        print("Button Pressed!")
    
    sleep(0.1)

