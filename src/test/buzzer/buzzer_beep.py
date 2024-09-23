from machine import Pin,PWM
from time import sleep

buzzer_Pin = Pin(12,Pin.OUT)
freq = 500                      
duty = 500                      

beep = PWM(buzzer_Pin,freq) 
beep.duty(duty)             
sleep(1)                        
beep.deinit()    
