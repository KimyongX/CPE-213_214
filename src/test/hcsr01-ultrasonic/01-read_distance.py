from machine import Pin, SoftI2C 
from hcsr04 import HCSR04 
from time import sleep 

sensor1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)

while True:
  distance1 = sensor1.distance_cm()
  distance2 = sensor2.distance_cm()
  print(f"Distance1:{distance1} Distance2:{distance2}")
  sleep(0.5)
  
