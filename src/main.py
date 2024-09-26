#---Import Library---
from time import sleep,localtime,time,sleep_ms
from ssd1306 import SSD1306_I2C
from machine import Pin,SoftI2C,PWM,RTC
from network import STA_IF,WLAN
import logging
from arduino_iot_cloud import ArduinoCloudClient
from hcsr04 import HCSR04
from servo import Servo
from ntptime import settime

#---Import Credential---
from secrets import WIFI_SSID
from secrets import WIFI_PASSWORD
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD
from secrets import LINE_NOTIFY_TOKEN

#---Function---
def beep(beeper,freq,duty,last):
    beeper = PWM(beeper,freq)
    beeper.duty(duty)
    sleep(last)
    beeper.duty(0)
    
def wifi_connect():
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASSWORD)
    oled.text('Waiting WIFI...',0,10)
    oled.show()
    while not wlan.isconnected():
        logging.info("Trying to connect to WIFI, Note this may take a while")
        sleep(0.5)
    logging.info("WIFI Connected!")
    logging.info(f"{wlan.ifconfig()}")
    oled.text('Waiting WIFI...',0,10,0)
    oled.show()
    oled.text('WIFI Connected!',0,10)
    oled.show()
    

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
        beep(buzzer,500,1000,0.5)

def onServoStateChange(client,value):
    print('Servo state from Arduino Cloud: {}'.format(value))
    
    if value == True:
        servo.write(90)
    else:
        servo.write(0)

def onServoAngleChange(client,value):
    print('Servo angle value from Arduino Cloud: {}'.format(value))
    
def onAlarmDateChange(client,value):
    print('Alarm Date Set to : {}'.format(value))

def onAlarmMonthChange(client,value):
    print('Alarm Month Set to : {}'.format(value))

def onAlarmYearChange(client,value):
    print('Alarm Year Set to : {}'.format(value))

def onAlarmHourChange(client,value):
    print('Alarm Hour Set to : {}'.format(value))

def onAlarmMinuteChange(client,value):
    print('Alarm Minute Set to : {}'.format(value))

def onAlarmSecondChange(client,value):
    print('Alarm Second Set to : {}'.format(value))

def onAlarmRepeatChange(client,value):
    print('Alarm Repeat Set to : {}'.format(value))

def onAlarmStateChange(client,value):
    print('Alarm Repeat Set to : {}'.format(value))

#---Pin Setup---
buzzer = Pin(12,Pin.OUT)
beep(buzzer,500,1000,0.5)

oled_Pin = SoftI2C(scl=Pin(22),sda=Pin(21))
oled_ScreenWidth = 128
oled_ScreenHeight = 64
oled = SSD1306_I2C(oled_ScreenWidth,oled_ScreenHeight,oled_Pin)

oled.fill(0)
oled.show()
oled.text('System begin...',0,0)
oled.show()

red_led = Pin(4,Pin.OUT)
green_led = Pin(2,Pin.OUT)
blue_led = Pin(15,Pin.OUT)

red_led.on()
green_led.off()
blue_led.off()

btn1_Pin = Pin(13,Pin.IN)

sensor1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)


servo = Servo(15)
servo.write(0)
    
wlan = WLAN(STA_IF)

logging.basicConfig(datefmt="%H:%M:%S",format="%(asctime)s.%(msecs)03d %(message)s",level=logging.INFO)
wifi_connect()

oled.text('Cloud Start...',0,30)
oled.show()

arduino_client = ArduinoCloudClient(device_id = DEVICE_ID,username=DEVICE_ID, password=CLOUD_PASSWORD,sync_mode=True)

arduino_client.register('message',value=None,on_write=onMessageChange)
arduino_client.register('distance1',value=None,on_read=readDistance1)
arduino_client.register('distance2',value=None,on_read=readDistance2)
arduino_client.register('buzzer_state',value=None,on_write=onBuzzerChange)
arduino_client.register('servo_state',value=None,on_write=onServoStateChange)
arduino_client.register('servo_angle',value=None,on_write=onServoAngleChange)

arduino_client.register('alarm_date',value=None,on_write=onAlarmDateChange)
arduino_client.register('alarm_month',value=None,on_write=onAlarmMonthChange)
arduino_client.register('alarm_year',value=None,on_write=onAlarmYearChange)

arduino_client.register('alarm_hour',value=None,on_write=onAlarmHourChange)
arduino_client.register('alarm_minute',value=None,on_write=onAlarmMinuteChange)
arduino_client.register('alarm_second',value=None,on_write=onAlarmSecondChange)

arduino_client.register('alarm_repeat',value=None,on_write=onAlarmRepeatChange)
arduino_client.register('alarm_state', value=None, on_write=onAlarmStateChange)

arduino_client.start()

oled.text('Cloud Start...',0,30,0)
oled.show()
oled.text('Cloud Connected!',0,30,1)
oled.show()


rtc = RTC()
settime()
current_time = localtime(time() + 7 * 3600)
rtc.datetime((current_time[0], current_time[1], current_time[2], 0, current_time[3], current_time[4], current_time[5], 0))
current_datetime = rtc.datetime()
print("Board's current time:", current_datetime)


oled.text('System Ready!',0,40)
oled.show()
sleep(1)

while True:
    arduino_client.update()
    
    current_datetime = rtc.datetime()
    year = current_datetime[0]
    month = current_datetime[1]
    date = current_datetime[2]
    hour = current_datetime[4]
    minute = current_datetime[5]
    second = current_datetime[6]
    oled.text("Time Now",0,0)
    oled.text("{}/{}/{}".format(date,month,year),0,10)
    oled.text("{}:{}:{}".format(hour,minute,second),0,20)
    oled.text("Feed Time",0,30)
    oled.show()
    oled.fill(0)
