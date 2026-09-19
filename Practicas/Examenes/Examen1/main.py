from machine import Pin, Timer
from time import ticks_ms, ticks_diff, sleep_ms


# LEDs
LED_RED = Pin(13, Pin.OUT)
LED_YELLOW = Pin(14, Pin.OUT)
LED_GREEN = Pin(15, Pin.OUT)

# Botones
BUTTON_A = Pin(16, Pin.IN, Pin.PULL_UP)
BUTTON_B = Pin(17, Pin.IN, Pin.PULL_UP)


# Estados
STATE_LOCKED = 0
STATE_WAITING = 1
STATE_ACCESS = 2
STATE_SECURITY = 3


state = STATE_LOCKED

failed_attempts = 0

last_irq_ms = 0


# Timers
timer_5s = Timer(-1)
timer_3s = Timer(-1)
timer_10s = Timer(-1)


# --------------------------------
# Estado BLOQUEADO
# --------------------------------

def locked():
    LED_RED.on()
    LED_YELLOW.off()
    LED_GREEN.off()

    print("")
    print("=================================")
    print("[LISTO] SISTEMA BLOQUEADO")
    print("Secuencia correcta: A -> B")
    print("=================================")


# --------------------------------
# Estado ESPERANDO B
# --------------------------------

def waiting():
    LED_RED.off()
    LED_YELLOW.on()
    LED_GREEN.off()

    print("[ESPERA] Presiona B antes de 5 segundos")


# --------------------------------
# Acceso concedido
# --------------------------------

def access():
    global failed_attempts

    LED_RED.off()
    LED_YELLOW.off()
    LED_GREEN.on()

    # Reiniciar intentos al conceder acceso
    failed_attempts = 0

    print("[OK] ACCESO CONCEDIDO")
    print("[RESET] Intentos fallidos = 0")
    print("[TIMER] Acceso activo durante 3 segundos")


# --------------------------------
# Tiempo de espera de B terminado
# --------------------------------

def timeout(t):
    global state

    if state == STATE_WAITING:

        print("[TIMEOUT] No se presiono B a tiempo")
        print("[ERROR] Intento fallido")

        failed()


# --------------------------------
# Acceso de 3 segundos terminado
# --------------------------------

def access_finished(t):
    global state

    print("")
    print("[TIMER] Fin del acceso")

    state = STATE_LOCKED
    locked()


# --------------------------------
# Bloqueo de seguridad terminado
# --------------------------------

def security_finished(t):
    global state, failed_attempts

    print("")
    print("[TIMER] Fin del bloqueo")

    failed_attempts = 0

    print("[RESET] Intentos fallidos = 0")

    state = STATE_LOCKED
    locked()


# --------------------------------
# Intento fallido
# --------------------------------

def failed():
    global state, failed_attempts

    failed_attempts += 1

    print("[ERROR] Intentos fallidos:", failed_attempts)

    state = STATE_LOCKED

    if failed_attempts >= 3:

        print("")
        print("[BLOQUEO] 3 errores detectados")
        print("[BLOQUEO] Sistema bloqueado 10 segundos")

        state = STATE_SECURITY

        timer_10s.init(
            mode=Timer.ONE_SHOT,
            period=10000,
            callback=security_finished
        )

    else:
        print("[LISTO] Intenta nuevamente con A -> B")
        locked()


# --------------------------------
# Botón A
# --------------------------------

def button_a_irq(pin):
    global state, last_irq_ms

    now = ticks_ms()

    # Anti-rebote
    if ticks_diff(now, last_irq_ms) < 80:
        return

    last_irq_ms = now

    # A funciona cuando está bloqueado
    if state == STATE_LOCKED:

        print("")
        print("[A] Boton A detectado")

        state = STATE_WAITING

        waiting()

        # Esperar B durante 5 segundos
        timer_5s.init(
            mode=Timer.ONE_SHOT,
            period=5000,
            callback=timeout
        )

    # A presionado mientras ya estamos esperando B
    elif state == STATE_WAITING:

        print("[INFO] A ignorado: ya se esta esperando B")

    # A presionado durante el bloqueo de seguridad
    elif state == STATE_SECURITY:

        print("[INFO] A ignorado: bloqueo de seguridad")


# --------------------------------
# Botón B
# --------------------------------

def button_b_irq(pin):
    global state, last_irq_ms

    now = ticks_ms()

    # Anti-rebote
    if ticks_diff(now, last_irq_ms) < 80:
        return

    last_irq_ms = now

    # B antes que A
    if state == STATE_LOCKED:

        print("")
        print("[ERROR] B fue presionado antes que A")

        failed()

    # B después de A
    elif state == STATE_WAITING:

        print("")
        print("[B] Boton B detectado")

        # Cancelar los 5 segundos
        timer_5s.deinit()

        state = STATE_ACCESS

        access()

        # Verde durante 3 segundos
        timer_3s.init(
            mode=Timer.ONE_SHOT,
            period=3000,
            callback=access_finished
        )

    # B durante el bloqueo de seguridad
    elif state == STATE_SECURITY:

        print("[INFO] B ignorado: bloqueo de seguridad")


# --------------------------------
# Interrupciones
# --------------------------------

BUTTON_A.irq(
    trigger=Pin.IRQ_FALLING,
    handler=button_a_irq
)

BUTTON_B.irq(
    trigger=Pin.IRQ_FALLING,
    handler=button_b_irq
)


# --------------------------------
# Inicio
# --------------------------------

locked()


while True:
    sleep_ms(20)
