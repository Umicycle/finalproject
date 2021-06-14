# 08_light_meter.py
# From the code for the Box 1 kit for the Raspberry Pi by MonkMakes.com

from guizero import App, Text
from gpiozero import DigitalOutputDevice, Button
import RPi.GPIO as GPIO
from PiAnalog import *
import time, math
import gpiozero
from gpiozero import Buzzer
p = PiAnalog()
pin1 = DigitalOutputDevice(24)
pin2 = DigitalOutputDevice(25)
p = PiAnalog()


multiplier = 20000 # increase to make more sensitive

def buzz(pitch, duration):
    period = 1.0 / pitch
    p2 = period / 2
    cycles = int(duration * pitch)
    for i in range(0, cycles):
        pin1.on()
        pin2.off()
        delay(p2)
        pin1.off()
        pin2.on()
        delay(p2)

def delay(p):
    t0 = time.time()


    while time.time() < t0 + p:
        pass


def light_from_r(R):
    light = 1/math.sqrt(R) * multiplier


    if light > 50:
        light = 100
        f = 2564/2
        buzz(f, 0.125)

    elif light < 50:
        light = 100
        f = 868*2
        buzz(f,1)
    return light







# group together all of the GUI code
# Update the reading
def update_reading():
    light = light_from_r(p.read_resistance())
    reading_str = "{:.0f}".format(light)
    light_text.value = reading_str
    light_text.after(200, update_reading)

app = App(title="Light Meter", width="400", height="300")
Text(app, text="Light", size=32)
light_text = Text(app, text="0", size=110)
light_text.after(200, update_reading)
app.display()