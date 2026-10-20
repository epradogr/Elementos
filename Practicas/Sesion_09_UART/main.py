# SESION 09 - SHOW 3 (CON NIVEL 3 · BONUS COMPACTO)
# Interfaz: Thonny por USB | Transporte probado: UART0 loopback GP0->GP1

from machine import UART, Pin, Timer
from time import sleep_ms, ticks_ms, ticks_diff

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Agrupar pines, timers y estado de parpadeo en una sola estructura
LEDS = {
    "LED1": {"pin": Pin(13, Pin.OUT, value=0), "timer": Timer(-1), "active": False},
    "LED2": {"pin": Pin(14, Pin.OUT, value=0), "timer": Timer(-1), "active": False},
}

MIN_MS, MAX_MS = 50, 5000  # Rango válido para BLINK (50 ms a 5 s)
TOGGLE_MS = 500            # Periodo fijo para TOGGLE


def get_targets(dev):
    if dev == "ALL":
        return list(LEDS.values())
    return [LEDS[dev]] if dev in LEDS else []


def set_led_mode(dev, val=None, period_ms=0):
    """Detiene cualquier timer previo y fija un estado (0/1) o inicia un parpadeo."""
    targets = get_targets(dev)
    if not targets:
        return False

    for item in targets:
        item["timer"].deinit()
        if period_ms > 0:
            pin = item["pin"]
            item["timer"].init(
                period=period_ms,
                mode=Timer.PERIODIC,
                callback=lambda t, p=pin: p.value(not p.value())
            )
            item["active"] = True
        else:
            item["active"] = False
            if val is not None:
                item["pin"].value(int(val))
    return True


def receive_complete_line(timeout_ms=1000):
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
    while uart.any():
        uart.read()
    uart.write((text + "\n").encode())
    return receive_complete_line(timeout_ms)


def handle_frame(frame):
    if not frame:
        return "ERR,EMPTY_FRAME"

    frame = frame.upper().strip()
    if frame == "PING":
        return "ACK,PONG"
    if frame == "GET,STATUS":
        return "STATUS,LED1,{},LED2,{}".format(LEDS["LED1"]["pin"].value(), LEDS["LED2"]["pin"].value())
    if frame == "HELP":
        return "ACK,CMDS:PING;GET,STATUS;SET,<DEV>,<0|1>;TOGGLE,<DEV>;BLINK,<DEV>,<50-5000|0>"

    parts = frame.split(",")
    cmd, dev = parts[0], parts[1] if len(parts) > 1 else ""

    if dev not in ("LED1", "LED2", "ALL"):
        return "ERR,DEVICE_NOT_FOUND"

    # TOGGLE,<DEV> -> Si está parpadeando lo apaga; si no, parpadea a 500 ms
    if len(parts) == 2 and cmd == "TOGGLE":
        is_active = any(x["active"] for x in get_targets(dev))
        if is_active:
            set_led_mode(dev, val=0, period_ms=0)
            return "ACK,TOGGLE,{},OFF".format(dev)
        set_led_mode(dev, period_ms=TOGGLE_MS)
        return "ACK,TOGGLE,{},ON".format(dev)

    if len(parts) == 3:
        param = parts[2]

        # SET,<DEV>,<0|1> (También apaga cualquier TOGGLE/BLINK activo)
        if cmd == "SET":
            if param not in ("0", "1"):
                return "ERR,INVALID_VALUE"
            set_led_mode(dev, val=param, period_ms=0)
            return "ACK,SET,{},{}".format(dev, param)

        # BLINK,<DEV>,<MS> (0 para apagar, o entre 50 y 5000 ms)
        if cmd == "BLINK":
            try:
                ms = int(param)
            except ValueError:
                return "ERR,INVALID_NUMBER"

            if ms == 0:
                set_led_mode(dev, val=0, period_ms=0)
                return "ACK,BLINK,{},OFF".format(dev)
            if not (MIN_MS <= ms <= MAX_MS):
                return "ERR,OUT_OF_RANGE,{}-{}".format(MIN_MS, MAX_MS)

            set_led_mode(dev, period_ms=ms)
            return "ACK,BLINK,{},{}".format(dev, ms)

    return "ERR,UNKNOWN_COMMAND"


print("SHOW 3 listo | Comandos: PING | GET,STATUS | SET,LED1,1 | TOGGLE,LED1 | BLINK,LED2,250 | HELP")

while True:
    try:
        command = input("CMD> ").strip()
    except KeyboardInterrupt:
        set_led_mode("ALL", val=0, period_ms=0)
        print("\nPrograma detenido")
        break

    if not command:
        continue

    received = uart_roundtrip(command)
    print("UART RX :", received if received else "SIN DATOS")
    if received:
        print("RESP    :", handle_frame(received))
