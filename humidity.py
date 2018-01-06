import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height - padding
x = 0

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
all_lights = [18,22,23]
GPIO.setup(all_lights,GPIO.OUT)

font = ImageFont.load_default()

def light_on(pin):
    GPIO.output(pin,GPIO.HIGH)

def light_off(pin):
    GPIO.output(pin,GPIO.LOW)

GPIO.output(all_lights,GPIO.LOW)
current_light = None

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    f_temp = (temperature * (9.0/5.0)) + 32
    #print 'Temp: {0:0.1f}F  Humidity: {1:0.1f}%'.format(f_temp, humidity)
    if current_light:
        light_off(current_light)
    if 0 <= humidity <= 24:
        light_on(22)
        current_light = 22
    elif 25 <= humidity <= 29:
        light_on(23)
        current_light = 23
    else:
        light_on(18)
        current_light = 18

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((2, top), "Humidity: {0:0.1f}".format(humidity), font=font, fill=255)
    draw.text((2, top+8), "Temp: {0:0.1f}F".format(f_temp), font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(1)
