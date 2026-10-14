# Sesión 08 - DO 08 COMPLETO
# Sistema multitarea cooperativa en Wokwi usando ticks_ms().
from machine import Pin, ADC
from time import ticks_ms, ticks_diff, sleep_ms

adc = ADC(26)
led_normal = Pin(13, Pin.OUT)
led_warning = Pin(14, Pin.OUT)
led_alarm = Pin(15, Pin.OUT)
heartbeat = Pin(12, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)

raw_value = 0
filtered_value = 0
percent_value = 0
state = "INIT"
sample_count = 0
alarm_ack = False
last_button = 1
alarm_blink = False

buffer = []
BUFFER_SIZE = 8

sensor_period = 20      # 50 Hz
ui_period = 200         # 5 Hz
log_period = 1000       # 1 Hz
button_period = 50      # 20 Hz

next_sensor = ticks_ms()
next_ui = ticks_ms()
next_log = ticks_ms()
next_button = ticks_ms()


def due(now, target):
    return ticks_diff(now, target) >= 0


def moving_average(new_value):
    # TODO 1: Buffer circular y promedio entero
    buffer.append(new_value)
    if len(buffer) > BUFFER_SIZE:
        buffer.pop(0)
    return sum(buffer) // len(buffer)


def classify(percent):
    # TODO 2: Clasificación de rangos
    if percent < 50:
        return "NORMAL"
    elif percent < 75:
        return "WARNING"
    else:
        return "ALARM"


def sensor_task():
    global raw_value, filtered_value, percent_value
    global state, sample_count, alarm_ack

    # TODO 3:
    # 1) Leer ADC
    raw_value = adc.read_u16()
    
    # 2) Filtrar con moving_average()
    filtered_value = moving_average(raw_value)
    
    # 3) Convertir a porcentaje usando el valor filtrado
    percent_value = (filtered_value * 100) / 65535
    
    # 4) Clasificar el estado
    new_state = classify(percent_value)
    
    # 5) Incrementar contador
    sample_count += 1
    
    # 6) Si desaparece la alarma, limpiar el ACK
    if new_state != "ALARM":
        alarm_ack = False

    state = new_state


def ui_task():
    global alarm_blink

    # TODO 4:
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

        if alarm_ack:
            led_alarm.on()
        else:
            alarm_blink = not alarm_blink
            led_alarm.value(alarm_blink)


def log_task():
    print("raw=", raw_value,
          "filtered=", filtered_value,
          "percent=", round(percent_value, 1),
          "state=", state,
          "samples=", sample_count,
          "ack=", alarm_ack)


def button_task():
    global alarm_ack, last_button

    current_button = button.value()

    # TODO 5: Flanco de bajada (1 -> 0)
    if last_button == 1 and current_button == 0:
        if state == "ALARM":
            alarm_ack = True
            print(">>> ALARMA RECONOCIDA | ACK=True")
        else:
            print(">>> Botón presionado, pero no hay ALARM")

    last_button = current_button


print("DO 08: sistema multitarea cooperativo completo")

while True:
    now = ticks_ms()

    if due(now, next_sensor):
        sensor_task()
        next_sensor = now + sensor_period

    if due(now, next_ui):
        ui_task()
        next_ui = now + ui_period

    if due(now, next_log):
        log_task()
        next_log = now + log_period

    if due(now, next_button):
        button_task()
        next_button = now + button_period

    sleep_ms(2)