from machine import Pin, SoftI2C 
from hcsr04 import HCSR04 
from time import sleep
import ssd1306, time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
width = 128 
height = 64 
display = ssd1306.SSD1306_I2C(width, height, i2c)
display.fill(0) 

sensor1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)

while True:
  distance1 = sensor1.distance_cm()
  distance2 = sensor2.distance_cm()

  display.text(f"Distance1:{distance1} cm.",0,0)
  display.text(f"Distance2:{distance2} cm.",0,10)
  display.show()
  display.fill(0)
  
  sleep(0.1)
