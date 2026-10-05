# Sesion 07 - DO 03 / Tarea
# Smart Analog Monitor - STARTER

from machine import Pin, ADC
from time import sleep_ms

sensor = ADC(Pin(26))
green = Pin(13, Pin.OUT)
yellow = Pin(14, Pin.OUT)
red = Pin(15, Pin.OUT)

VREF = 3.3
WARNING = 50
ALARM = 75
WINDOW_SIZE = 10
window = []

def read_raw():
    return sensor.read_u16()

def to_voltage(raw):
    # Convertir raw 65535 a voltaje 0-3.3V
    return raw * VREF / 65535

def to_percent(raw):
    # Convertir raw  a porcentaje 
    return raw * 100 / 65535

def filter_average(raw):
    # Agregar raw a la ventana y regresar promedio
    window.append(raw)
    if len(window) > WINDOW_SIZE:
        window.pop(0)
    return sum(window) / len(window)

def classify(percent):
    # Regresar NORMAL, WARNING o ALARM
    if percent >= ALARM:
        return "ALARM"
    elif percent >= WARNING:
        return "WARNING"
    else:
        return "NORMAL"

def update_outputs(state):
    # Encender solo el LED que corresponde evaluando booleanos
    green.value(state == "NORMAL")
    yellow.value(state == "WARNING")
    red.value(state == "ALARM")

def print_status(raw, filtered, voltage, percent, state):
    print("raw:", raw, "| filtered:", int(filtered), "| V:", round(voltage, 2), "| %:", round(percent, 1), "| state:", state)

print("CHALLENGE 07 - Smart Analog Monitor")

while True:
    raw = read_raw()
    filtered = filter_average(raw)
    voltage = to_voltage(filtered)
    percent = to_percent(filtered)
    state = classify(percent)
    update_outputs(state)
    print_status(raw, filtered, voltage, percent, state)
    sleep_ms(300)
