# Sesión 08 - SHOW 2 MEJORADO
# Prueba física con Raspberry Pi Pico / Pico W / Pico 2 W.
# Core 1: adquisición rápida del ADC.
# Core 0: interfaz, botón, heartbeat y terminal con periodos independientes.

from machine import Pin, ADC
from time import ticks_ms, ticks_diff, sleep_ms
import _thread

adc = ADC(26)
led_normal = Pin(13, Pin.OUT)
led_warning = Pin(14, Pin.OUT)
led_alarm = Pin(15, Pin.OUT)
heartbeat = Pin(12, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)

lock = _thread.allocate_lock()

shared = {
    "raw": 0,
    "percent": 0.0,
    "state": "INIT",
    "samples": 0,
    "ack": False,
}

last_button = 1
alarm_blink = False

ui_period = 200
button_period = 50
log_period = 1000

next_ui = ticks_ms()
next_button = ticks_ms()
next_log = ticks_ms()


def due(now, target):
    return ticks_diff(now, target) >= 0


def classify(percent):
    if percent < 50:
        return "NORMAL"
    elif percent < 75:
        return "WARNING"
    else:
        return "ALARM"


def sensor_core():
    # CORE 1: tarea crítica rápida de adquisición.
    while True:
        raw = adc.read_u16()
        percent = raw * 100 / 65535
        state = classify(percent)

        lock.acquire()
        shared["raw"] = raw
        shared["percent"] = percent
        shared["state"] = state
        shared["samples"] += 1
        if state != "ALARM":
            shared["ack"] = False
        lock.release()

        sleep_ms(20)  # ~50 muestras/s


def read_shared():
    lock.acquire()
    snapshot = (
        shared["raw"],
        shared["percent"],
        shared["state"],
        shared["samples"],
        shared["ack"],
    )
    lock.release()
    return snapshot


def ui_task():
    global alarm_blink

    raw, percent, state, samples, ack = read_shared()
    heartbeat.toggle()

    if state == "NORMAL":
        led_normal.on()
        led_warning.off()
        led_alarm.off()

    elif state == "WARNING":
        led_normal.off()
        led_warning.on()
        led_alarm.off()

    elif state == "ALARM":
        led_normal.off()
        led_warning.off()
        if ack:
            led_alarm.on()
        else:
            alarm_blink = not alarm_blink
            led_alarm.value(alarm_blink)


def button_task():
    global last_button

    current = button.value()

    if last_button == 1 and current == 0:
        lock.acquire()
        if shared["state"] == "ALARM":
            shared["ack"] = True
            accepted = True
        else:
            accepted = False
        lock.release()

        if accepted:
            print(">>> CORE 0: ALARMA RECONOCIDA")
        else:
            print(">>> CORE 0: botón sin alarma activa")

    last_button = current


def log_task():
    raw, percent, state, samples, ack = read_shared()
    print("CORE0 UI | raw=", raw,
          "percent=", round(percent, 1),
          "state=", state,
          "samples_core1=", samples,
          "ack=", ack)


print("Iniciando adquisición en Core 1...")
_thread.start_new_thread(sensor_core, ())
print("Core 0 mantiene UI, botón y serial.")

while True:
    now = ticks_ms()

    if due(now, next_ui):
        ui_task()
        next_ui = now + ui_period

    if due(now, next_button):
        button_task()
        next_button = now + button_period

    if due(now, next_log):
        log_task()
        next_log = now + log_period

    sleep_ms(2)