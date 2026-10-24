# EXAMEN PRÁCTICO 02

from machine import Pin, ADC, PWM, UART
from time import ticks_ms, ticks_diff, sleep_ms
import _thread

adc = ADC(Pin(26))
led_digital = Pin(13, Pin.OUT)
led_pwm = PWM(Pin(15))
led_pwm.freq(1000)
led_pwm.duty_u16(0)

button = Pin(16, Pin.IN, Pin.PULL_UP)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

WINDOW_SIZE = 10
window = []
pwm_value = 0

lock = _thread.allocate_lock()

shared = {
    "raw": 0,
    "percent": 0.0,
    "samples": 0,
}


def to_percent(raw):
    # Convertir raw a porcentaje 
    return raw * 100 / 65535


def filter_average(raw):
    # Agregar raw a la ventana y regresar promedio 
    window.append(raw)
    if len(window) > WINDOW_SIZE:
        window.pop(0)
    return sum(window) / len(window)


def read_shared():
    # Lectura segura con lock 
    lock.acquire()
    snapshot = (
        shared["raw"],
        shared["percent"],
        shared["samples"],
    )
    lock.release()
    return snapshot


def sensor_core():
    # CORE 1: tarea crítica rápida de adquisición y botón (De Sesión 08)
    last_button = 1

    while True:
        raw = adc.read_u16()
        filtered = filter_average(raw)
        percent = to_percent(filtered)

        lock.acquire()
        shared["raw"] = raw
        shared["percent"] = percent
        shared["samples"] += 1
        lock.release()

        current = button.value()
        if last_button == 1 and current == 0:
            _, pct, samples = read_shared()
            print(
                "\nSTATUS,LED={},PWM={},ADC={},BTN={},SAMPLES={}".format(
                    led_digital.value(), pwm_value, round(pct, 1), current, samples
                )
            )
        last_button = current

        sleep_ms(20)  # 


def receive_complete_line(timeout_ms=1000):
    # Recepción por UART 
    buffer = bytearray()
    start = ticks_ms()
    while ticks_diff(ticks_ms(), start) < timeout_ms:
        while uart.any():
            byte = uart.read(1)
            if byte == b"\n":
                return buffer.decode().rstrip("\r")
            if byte:
                buffer.extend(byte)
        sleep_ms(1)
    return None


def uart_roundtrip(text, timeout_ms=1000):
    # Envío y recepción loopback UART 
    while uart.any():
        uart.read()
    uart.write((text + "\n").encode())
    return receive_complete_line(timeout_ms)


def handle_frame(frame):
    # Parser de comandos 
    global pwm_value

    if not frame:
        return "ERR,BAD_FORMAT"

    frame = frame.upper().strip()

    if frame == "PING":
        return "PONG"

    if frame == "STATUS":
        _, percent, samples = read_shared()
        return "STATUS,LED={},PWM={},ADC={},BTN={},SAMPLES={}".format(
            led_digital.value(), pwm_value, round(percent, 1), button.value(), samples
        )

    parts = frame.split(",")
    cmd = parts[0]

    if cmd in ("LED", "PWM", "ALL"):
        if len(parts) != 2 or parts[1] == "":
            return "ERR,BAD_FORMAT"

        param = parts[1]

        if cmd == "LED":
            if param not in ("0", "1"):
                return "ERR,BAD_VALUE"
            led_digital.value(int(param))
            return "ACK,LED,{}".format(param)

        if cmd == "PWM":
            try:
                n = int(param)
            except ValueError:
                return "ERR,BAD_VALUE"

            if not (0 <= n <= 100):
                return "ERR,PWM_RANGE"

            pwm_value = n
            led_pwm.duty_u16(int(n * 65535 / 100))
            return "ACK,PWM,{}".format(n)

        if cmd == "ALL":
            if param not in ("0", "1"):
                return "ERR,BAD_VALUE"
            val = int(param)
            led_digital.value(val)
            pwm_value = 100 if val == 1 else 0
            led_pwm.duty_u16(65535 if val == 1 else 0)
            return "ACK,ALL,{}".format(val)

    return "ERR,UNKNOWN_COMMAND"

 
print("Iniciando adquisición en Core 1...")
_thread.start_new_thread(sensor_core, ())
print("EXAMEN 02 listo | Comandos: PING | LED,0/1 | PWM,0-100 | STATUS | ALL,0/1")

while True:
    try:
        command = input("CMD> ").strip()
    except KeyboardInterrupt:
        led_digital.value(0)
        led_pwm.duty_u16(0)
        print("\nPrograma detenido")
        break

    if not command:
        continue

    received = uart_roundtrip(command)
    print("UART RX :", received if received else "SIN DATOS")
    if received:
        print("RESP    :", handle_frame(received))
