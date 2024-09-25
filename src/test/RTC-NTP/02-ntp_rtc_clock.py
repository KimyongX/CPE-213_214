# Import Library
from ssd1306 import SSD1306_I2C
from machine import Pin,SoftI2C,RTC,PWM
from time import sleep,localtime,time
from network import STA_IF,WLAN
from ntptime import settime

# Network Credential
ssid = 'your_credential'
password = 'your_creadential'

# Pin Setup
oled_Pin = SoftI2C(scl=Pin(22),sda=Pin(21))
buzzer = Pin(32, Pin.OUT)

# RTC
rtc = RTC()
print("Board's current time:", rtc.datetime())

# Alarm time
alarm_hour = 16
alarm_minute = 33
alarm_second = 0

# Screen Resolution 
oled_ScreenWidth = 128
oled_ScreenHeight = 64

# OLED Interface 
oled = SSD1306_I2C(oled_ScreenWidth,oled_ScreenHeight,oled_Pin)

# Network Interface 
wlan = WLAN(STA_IF)
# Activate the station mode
wlan.active(True)
# Check if the devices are already connected or not.
# If it is not connected, then start the connection.
if not wlan.isconnected():
   print("Connecting to wifi: ", ssid)
   wlan.connect(ssid, password)
   # Wait until your devices are connected.
   while not wlan.isconnected():
       pass
print("Connection successful")

# Connection Config
print(wlan.ifconfig())


#---Automatically fetches time from NTP server---
print("Fetching time from NTP server...")
settime()

#---Adjust for Asia/Bangkok timezone (UTC+7)---
current_time = localtime(time() + 7 * 3600)
rtc.datetime((current_time[0], current_time[1], current_time[2], 0, current_time[3], current_time[4], current_time[5], 0))
current_datetime = rtc.datetime()

while True:
    current_datetime = rtc.datetime()
    year = current_datetime[0]
    month = current_datetime[1]
    date = current_datetime[2]
    hour = current_datetime[4]
    minute = current_datetime[5]
    second = current_datetime[6]
    oled.text("RTC",0,0)
    oled.text("{}/{}/{}".format(date,month,year),0,10)
    oled.text("{}:{}:{}".format(hour,minute,second),0,20)
    oled.show()
    oled.fill(0)
    
    if hour == alarm_hour and minute == alarm_minute and second == alarm_second:
        beep = PWM(buzzer,1000)
        beep.duty(1000)
        sleep(0.5)  
        beep.deinit()  

