import RPi.GPIO as GPIO
import time
from bottle import route, run, template, static_file
import sys
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import adcUtil as adc
import Adafruit_DHT
import dht11
import pigpio


print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)
os.system("")
proc = subprocess.Popen(["./camLoop.sh"])
dates = []
times = []
types = []


@route('/')
def index():
    html = open('index.html').read()
    html = html.replace("<{weekago}>", (datetime.today()-timedelta(7)).strftime("%b %d, %y"))
    html = html.replace("<{monthago}>", (datetime.today()-timedelta(30)).strftime("%b %d, %y"))
    
    pi = pigpio.pi()
    sensor = DHT11(pi, 4)
    temperature = None
    humidity = None
    for response in sensor:
        temperature = response['temperature']
        humidity = humidity['humidity']
    sensor.close()
    
    html = html.replace("<{Temperature}>", temperature)
    html = html.replace("<{Humidity}>", humidity)

    Vou_photoresist = adc.readADC(channel=0)
    html = html.replace("<{Light Intensity}>", Vou_photoresist / 2)
    
    generateWeek()
    generateMonth()
    generateDayLoad()
    generateMonthDrive()
    
    html = replaceEvents(html)
    
    return html


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')


def generateWeek():
    arr = np.random.randint(40, 80, 29)
    hum = np.random.randint(15, 95, 29)
    light = np.random.randint(0, 100, 29)
    t = np.arange(datetime.today()-timedelta(7), datetime.today(), timedelta(days=0.25)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr, label="Temp")
    plt.plot(t, hum, label="Humdity %")
    plt.plot(t, light, label="Light %")
    plt.legend()
    plt.savefig("static/weekWeather.png", format="png")
    
    
def generateMonth():
    arr = np.random.randint(40, 80, 30+1)
    hum = np.random.randint(15, 95, 30+1)
    light = np.random.randint(0, 100, 30+1)
    t = np.arange(datetime.today()-timedelta(30), datetime.today(), timedelta(days=1)).astype(datetime)
    plt.figure(figsize=(10,4))
    plt.plot(t, arr, label="Temp")
    plt.plot(t, hum, label="Humdity %")
    plt.plot(t, light, label="Light %")
    plt.legend()
    plt.savefig("static/monthWeather.png", format="png")
    

def generateDayLoad():
    arr = np.random.randint(5, 25, int((24*60)/5+1))
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

