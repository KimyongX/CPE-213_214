#---Import Library---
from time import sleep, localtime, time, sleep_ms
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C, PWM, RTC,
from network import WLAN, STA_IF
import logging
from arduino_iot_cloud import ArduinoCloudClient
from hcsr04 import HCSR04
from servo import Servo
from ntptime import settime
from linenotify import LineNotify
from gc import collect

WIFI_SSID = "PX_SYSTEM_2.4G"
WIFI_PASSWORD = "PX123456789"
DEVICE_ID = b"e9bc8a01-13d8-4547-8ed9-dfb2b8a3e3e8"
CLOUD_PASSWORD = b"q0bRO#bFz427BZSSeA#6PyAPG"

#---Function Definitions---
def map(source, source_min, source_max, output_min, output_max):
    return int((source - source_min) * (output_max - output_min) / (source_max - source_min) + output_min)

def beep(beeper, freq, duty, last):
    beeper = PWM(beeper, freq)
    beeper.duty(duty)
    sleep(last)
    beeper.duty(0)

def wifi_connect():
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    oled.text('Waiting WIFI...', 0, 10)
    oled.show()
    while not wlan.isconnected():
        logging.info("Trying to connect to WIFI, Note this may take a while")
        sleep(0.5)
    logging.info("WIFI Connected!")
    logging.info(f"{wlan.ifconfig()}")
    oled.text('Waiting WIFI...', 0, 10, 0)
    oled.show()
    oled.text('WIFI Connected!', 0, 10)
    oled.show()

def readDistance1(client):
    distance1 = sensor1.distance_cm()
    distance1 = map(distance1, 3, 14, 100, 0)
    return distance1

def readDistance2(client):
    distance2 = sensor2.distance_cm()
    return distance2

def onMessageChange(client, value):
    print('Message from Arduino Cloud:{}'.format(value))

def onBuzzerChange(client, value):
    print('Buzzer value from Arduino Cloud: {}'.format(value))
    if value == True:
        beep(buzzer, 500, 1000, 0.5)

def onServoStateChange(client, value):
    print('Servo state from Arduino Cloud: {}'.format(value))
    if value == True:
        servo.write(30)
        blue_led.value(1)
    else:
        servo.write(110)
        blue_led.value(0)

def onServoAngleChange(client, value):
    print('Servo angle value from Arduino Cloud: {}'.format(value))

def onAlarmDateChange(client, value):
    global alarm_day
    print('Alarm Date Set to : {}'.format(value))
    alarm_day = value

def onAlarmMonthChange(client, value):
    global alarm_month
    print('Alarm Month Set to : {}'.format(value))
    alarm_month = value

def onAlarmYearChange(client, value):
    global alarm_year
    print('Alarm Year Set to : {}'.format(value))
    alarm_year = value

def onAlarmHourChange(client, value):
    global alarm_hour
    print('Alarm Hour Set to : {}'.format(value))
    alarm_hour = value

def onAlarmMinuteChange(client, value):
    global alarm_minute
    print('Alarm Minute Set to : {}'.format(value))
    alarm_minute = value

def onAlarmSecondChange(client, value):
    global alarm_second
    print('Alarm Second Set to : {}'.format(value))
    alarm_second = value

def onAlarmRepeatChange(client, value):
    global alarm_repeat
    print('Alarm Repeat Set to : {}'.format(value))
    alarm_repeat = value

def onAlarmRepeatValueChange(client, value):
    global alarm_repeat_value
    print('Alarm Repeat Value Set to : {}'.format(value))
    alarm_repeat_value = value

def onAlarmStateChange(client, value):
    print('Alarm State Set to : {}'.format(value))

def foodFeed():
    servo.write(30)
    blue_led.value(1)
    sleep(0.5)
    servo.write(110)
    blue_led.value(0)

def updateFeedTime():
    current_datetime = rtc.datetime()
    year, month, day = current_datetime[0], current_datetime[1], current_datetime[2]
    hour, minute, second = current_datetime[4], current_datetime[5], current_datetime[6]
    arduino_client["alarm_year"], arduino_client["alarm_month"], arduino_client["alarm_date"] = current_datetime[0], current_datetime[1], current_datetime[2]

    if arduino_client["alarm_repeat"] == 1:
        arduino_client["alarm_hour"], arduino_client["alarm_minute"], arduino_client["alarm_second"] = current_datetime[4], current_datetime[5] + arduino_client["alarm_repeat_value"], current_datetime[6]
    elif arduino_client["alarm_repeat"] == 2:
        arduino_client["alarm_hour"], arduino_client["alarm_minute"], arduino_client["alarm_second"] = current_datetime[4] + arduino_client["alarm_repeat_value"], current_datetime[5], current_datetime[6]

# Button Interrupt Handler
def button_handler(pin):
    print("Button pressed!")
    foodFeed()
    
#---Pin Setup---
buzzer = Pin(12, Pin.OUT)
beep(buzzer, 500, 1000, 0.5)

oled_pin = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_screen_width = 128
oled_screen_height = 64
oled = SSD1306_I2C(oled_screen_width, oled_screen_height, oled_pin)

oled.fill(0)
oled.show()
oled.text('System begin...', 0, 0)
oled.show()

red_led = Pin(4, Pin.OUT)
green_led = Pin(2, Pin.OUT)
blue_led = Pin(15, Pin.OUT)

red_led.on()
green_led.off()
blue_led.off()

# Button Setup
btn1_pin = Pin(13, Pin.IN, Pin.PULL_DOWN)
# Configure button interrupt
btn1_pin.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# HC-SR04 Setup
sensor1 = HCSR04(trigger_pin=25, echo_pin=33, echo_timeout_us=20000)
sensor2 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=20000)

# Servo Setup
servo = Servo(14)
servo.write(100)

# WiFi Setup
wlan = WLAN(STA_IF)

# Logging Setup
logging.basicConfig(datefmt="%H:%M:%S", format="%(asctime)s.%(msecs)03d %(message)s", level=logging.INFO)
wifi_connect()

oled.text('Cloud Start...', 0, 30)
oled.show()

# Arduino Cloud Setup
arduino_client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=CLOUD_PASSWORD, sync_mode=True)

# Register Cloud Variables
arduino_client.register('message', value=None, on_write=onMessageChange)
arduino_client.register('distance1', value=None, on_read=readDistance1)
arduino_client.register('distance2', value=None, on_read=readDistance2)
arduino_client.register('buzzer_state', value=None, on_write=onBuzzerChange)
arduino_client.register('servo_state', value=None, on_write=onServoStateChange)
arduino_client.register('servo_angle', value=None, on_write=onServoAngleChange)

arduino_client.register('alarm_date', value=None, on_write=onAlarmDateChange)
arduino_client.register('alarm_month', value=None, on_write=onAlarmMonthChange)
arduino_client.register('alarm_year', value=None, on_write=onAlarmYearChange)
arduino_client.register('alarm_hour', value=None, on_write=onAlarmHourChange)
arduino_client.register('alarm_minute', value=None, on_write=onAlarmMinuteChange)
arduino_client.register('alarm_second', value=None, on_write=onAlarmSecondChange)
arduino_client.register('alarm_repeat', value=None, on_write=onAlarmRepeatChange)
arduino_client.register('alarm_repeat_value', value=None, on_write=onAlarmRepeatValueChange)
arduino_client.register('alarm_state', value=None, on_write=onAlarmStateChange)

arduino_client.start()

oled.text('Cloud Start...', 0, 30, 0)
oled.show()
oled.text('Cloud Connected!', 0, 30, 1)
oled.show()

# RTC Setup
rtc = RTC()
settime()
current_time = localtime(time() + 7 * 3600)
rtc.datetime((current_time[0], current_time[1], current_time[2], 0, current_time[3], current_time[4], current_time[5], 0))
current_datetime = rtc.datetime()
print("Board's current time:", current_datetime)

oled.text('System Ready!', 0, 40)
oled.show()
arduino_client["message"] = "ระบบเริ่มต้นการทำงาน"
sleep(1)

updateFeedTime()


    

#---Main Loop---
while True:
    collect()
    arduino_client.update()
    
    # Update current datetime from RTC
    current_datetime = rtc.datetime()
    year, month, day = current_datetime[0], current_datetime[1], current_datetime[2]
    hour, minute, second = current_datetime[4], current_datetime[5], current_datetime[6]

    # Display current time on OLED
    oled.text("Time Now", 0, 0)
    oled.text("{}/{}/{}".format(day, month, year), 0, 10)
    oled.text("{}:{}:{}".format(hour, minute, second), 0, 20)
    oled.text("Time Feed", 0, 30)
    oled.text("{}/{}/{}".format(alarm_day, alarm_month, alarm_year), 0, 40)
    oled.text("{}:{}:{}".format(alarm_hour, alarm_minute, alarm_second), 0, 50)
    oled.show()
    oled.fill(0)
    
    # Alarm Check with Date and Time
    if (alarm_year is not None and alarm_month is not None and alarm_day is not None and 
        alarm_hour is not None and alarm_minute is not None and alarm_second is not None):
        if (year == alarm_year and month == alarm_month and day == alarm_day and 
            hour == alarm_hour and minute == alarm_minute and second == alarm_second):
            print("Alarm Triggered!")
            beep(buzzer, 500, 1000, 0.5)
            foodFeed()
            updateFeedTime()
                
    # WiFi reconnection
    if not wlan.isconnected():
        logging.info("WIFI lost. Reconnecting...")
        wifi_connect()

    sleep(0.1)  # Small delay to avoid high CPU usage
