import RPi.GPIO as GPIO
import time
import serial
from bottle import route, run, template
import sys
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, False)   

@route('/garage/:ledstate')
def ledtrigger(ledstate=0):
    if ledstate == 'activate':
        ser.write("activate\n")
        print("triggered")
        time.sleep(5)
        return 'garage button pressed'
    elif ledstate == 'reset':
        GPIO.output(3, False)
        return 'garage button reset'

run(host='0.0.0.0', port=6969)

