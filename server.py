import RPi.GPIO as GPIO
import time
from bottle import route, run, template, static_file
import sys
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import adcUtil as adc
from dht11 import DHT11
import pigpio


print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)
dates = []
times = []
types = []
GPIO.cleanup()
prevTemp = 0
prevHumidity = 0



@route('/')
def index():
    global prevTemp
    global prevHumidity
    print("LOADING")
    html = open('index.html').read()
    html = html.replace("<{weekago}>", (datetime.today()-timedelta(7)).strftime("%b %d, %y"))
    html = html.replace("<{monthago}>", (datetime.today()-timedelta(30)).strftime("%b %d, %y"))
    pi = pigpio.pi(port = 8887)
    sensor = DHT11(pi, 4)
    sensor.next()
    temperature, humidity = sensor.temperature, sensor.humidity
    if(temperature == 0 and humidity == 0):
        temperature, humidity = prevTemp, prevHumidity
    else:
        prevTemp, prevHumidity = temperature, humidity
        
    sensor.close()
    pi.stop()
    
    html = html.replace("<{Temperature}>", str(int(temperature*9/5+32)))
    html = html.replace("<{Humidity}>", str(humidity))

    Vou_photoresist = adc.readADC(channel=0)
    print(Vou_photoresist)
    html = html.replace("<{Light Intensity}>", str(int(100*Vou_photoresist / 2.6)))
    
    generateWeek()
    generateMonth()
    generateDayLoad()
    generateMonthDrive()
    plt.close(fig="all")

    html = replaceEvents(html)
    
    return html


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')


def generateWeek():
    arr = np.random.randint(40, 60, 29)
    hum = np.random.randint(15, 30, 29)
    light = np.random.randint(5, 20, 29)
    t = np.arange(datetime.today()-timedelta(7), datetime.today(), timedelta(days=0.25)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr, label="Temp")
    plt.plot(t, hum, label="Humdity %")
    plt.plot(t, light, label="Light %")
    plt.legend()
    plt.savefig("static/weekWeather.png", format="png")
    
    
def generateMonth():
    arr = np.random.randint(40, 60, 30+1)
    hum = np.random.randint(15, 30, 30+1)
    light = np.random.randint(5, 20, 30+1)
    t = np.arange(datetime.today()-timedelta(30), datetime.today(), timedelta(days=1)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr, label="Temp")
    plt.plot(t, hum, label="Humdity %")
    plt.plot(t, light, label="Light %")
    plt.legend()
    plt.savefig("static/monthWeather.png", format="png")
    

def generateDayLoad():
    arr = np.random.randint(5, 10, int((24*60)/5+1))
    t = np.arange(datetime.today()-timedelta(1), datetime.today(), timedelta(minutes=5)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr)
    plt.savefig("static/dayLoad.png", format="png")
    

def generateMonthDrive():
    arr = np.arange(30, 70, (70-30)/31)
    t = np.arange(datetime.today()-timedelta(30), datetime.today(), timedelta(days=1)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr)
    plt.savefig("static/monthDrive.png", format="png")
    

def replaceEvents(html):
    for i in range(1,6):
        try:
            dateRplStr = "<{e"+str(i)+"date}>"
            typeRplStr = "<{e"+str(i)+"type}>"
            timeRplStr = "<{e"+str(i)+"time}>"
            viewRplStr = "<{e"+str(i)+"view}>"
            dateRpl = dates[i-1].strftime("%m-%d-%y %H:%M:%S")
            typeRpl = types[i-1]
            timeRpl = times[i-1].strftime("%H:%M:%S")
            viewRpl = ""
        except IndexError:
            dateRpl = "XX-XX-XX --:--:--"
            typeRpl = "no"
            timeRpl = ""
            viewRpl = "style=\"display:none;\""
        
        html = html.replace(dateRplStr, dateRpl)
        html = html.replace(typeRplStr, typeRpl)
        html = html.replace(timeRplStr, timeRpl)
        html = html.replace(viewRplStr, viewRpl)
        
    return html

run(host='0.0.0.0', port=8080)

