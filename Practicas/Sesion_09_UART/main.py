# SESION 09 - SHOW 3 (CON NIVEL 3 · BONUS IMPLEMENTADO)
# Interfaz: Thonny por USB | Transporte probado: UART0 loopback GP0->GP1

from machine import UART, Pin
from time import sleep_ms, ticks_ms, ticks_diff

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
led1 = Pin(13, Pin.OUT)
led2 = Pin(14, Pin.OUT)

# Inicializar pines en bajo
led1.value(0)
led2.value(0)


def clear_rx():
    """Vacía datos viejos del buffer RX antes de una nueva prueba."""
    while uart.any():
        uart.read()


def receive_complete_line(timeout_ms=1000):
    """
    Lee byte por byte hasta encontrar '\n'.
    Evita procesar una trama parcial cuando uart.any() se activa
    apenas llega el primer carácter.
    """
    buffer = bytearray()
    start = ticks_ms()

    while ticks_diff(ticks_ms(), start) < timeout_ms:
        while uart.any():
            byte = uart.read(1)

            if not byte:
                break

            if byte == b"\n":
                return buffer.decode().rstrip("\r")

            buffer.extend(byte)

        sleep_ms(1)

    return None


def uart_roundtrip(text, timeout_ms=1000):
    clear_rx()
    uart.write((text + "\n").encode())
    return receive_complete_line(timeout_ms)


def status_frame():
    return "STATUS,LED1,{},LED2,{}".format(led1.value(), led2.value())


def set_output(device, value):
    output_value = int(value)
    if device == "LED1":
        led1.value(output_value)
        return True
    if device == "LED2":
        led2.value(output_value)
        return True
    if device == "ALL":
        led1.value(output_value)
        led2.value(output_value)
        return True
    return False


def toggle_output(device):
    if device == "LED1":
        led1.value(not led1.value())
        return str(led1.value())
    if device == "LED2":
        led2.value(not led2.value())
        return str(led2.value())
    if device == "ALL":
        # Invertir cada uno respecto a su propio estado
        led1.value(not led1.value())
        led2.value(not led2.value())
        return "{}:{}".format(led1.value(), led2.value())
    return None


def blink_output(device, ms):
    if device == "LED1":
        led1.value(1)
        sleep_ms(ms)
        led1.value(0)
        return True
    if device == "LED2":
        led2.value(1)
        sleep_ms(ms)
        led2.value(0)
        return True
    if device == "ALL":
        led1.value(1)
        led2.value(1)
        sleep_ms(ms)
        led1.value(0)
        led2.value(0)
        return True
    return False


def handle_frame(frame):
    if not frame:
        return "ERR,EMPTY_FRAME"

    frame = frame.upper().strip()

    # Nivel 1: PING y GET,STATUS
    if frame == "PING":
        return "ACK,PONG"

    if frame == "GET,STATUS":
        return status_frame()

    # Nivel 3 (Bonus): HELP
    if frame == "HELP":
        return "ACK,CMDS:PING;GET,STATUS;SET,<DEV>,<0|1>;TOGGLE,<DEV>;BLINK,<DEV>,<MS>"

    parts = frame.split(",")

    # Validación de comandos de 3 campos: SET y BLINK
    if len(parts) == 3:
        cmd, dev, param = parts

        # Nivel 1 & 2: SET,<DEV>,<0|1>
        if cmd == "SET":
            if dev not in ("LED1", "LED2", "ALL"):
                return "ERR,DEVICE_NOT_FOUND"
            if param not in ("0", "1"):
                return "ERR,INVALID_VALUE"
            set_output(dev, param)
            return "ACK,{},{}".format(dev, param)

        # Nivel 3 (Bonus): BLINK,<DEV>,<TIME_MS>
        if cmd == "BLINK":
            if dev not in ("LED1", "LED2", "ALL"):
                return "ERR,DEVICE_NOT_FOUND"
            try:
                ms = int(param)
                if ms <= 0:
                    return "ERR,INVALID_MS"
            except ValueError:
                return "ERR,INVALID_NUMBER"

            blink_output(dev, ms)
            return "ACK,BLINK,{},{}".format(dev, ms)

        return "ERR,UNKNOWN_COMMAND"

    # Validación de comandos de 2 campos: TOGGLE,<DEV>
    if len(parts) == 2:
        cmd, dev = parts
        if cmd == "TOGGLE":
            if dev not in ("LED1", "LED2", "ALL"):
                return "ERR,DEVICE_NOT_FOUND"
            new_state = toggle_output(dev)
            return "ACK,TOGGLE,{},{}".format(dev, new_state)

        return "ERR,UNKNOWN_COMMAND"

    return "ERR,UNKNOWN_FRAME"


print("SHOW 3 listo - UART Command Center (Bonus Activo)")
print("Jumper requerido: GP0(TX) -> GP1(RX)")
print("Comandos disponibles: PING | GET,STATUS | SET,LED1,1 | TOGGLE,LED1 | BLINK,LED2,500 | HELP")

while True:
    try:
        command = input("CMD> ").strip()
    except KeyboardInterrupt:
        print("\nPrograma detenido")
        break

    if not command:
        continue

    print("USB CMD :", command)
    received = uart_roundtrip(command)

    if received is None:
        print("UART RX : SIN DATOS. Revisa GP0->GP1")
        continue

    print("UART RX :", received)
    print("RESP    :", handle_frame(received))
