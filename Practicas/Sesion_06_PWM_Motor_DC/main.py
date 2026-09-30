from machine import Pin, PWM
from time import sleep_ms

# salidas
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
ENA = PWM(Pin(4))
ENA.freq(1000)

# botones
btn_fwd = Pin(14, Pin.IN, Pin.PULL_UP)
btn_rev = Pin(15, Pin.IN, Pin.PULL_UP)
btn_stop = Pin(16, Pin.IN, Pin.PULL_UP)

IN1.value(0)
IN2.value(0)

# Variables para recordar cómo está el motor en todo momento
estado = "STOP"      
vel_actual = 0       

def set_speed(percent):
    global vel_actual
    percent = max(0, min(100, percent))
    duty = int(percent * 65535 / 100)
    ENA.duty_u16(duty)
    vel_actual = percent

def forward():
    IN1.value(1)
    IN2.value(0)

def reverse():
    IN1.value(0)
    IN2.value(1)

def stop():
    set_speed(0)
    IN1.value(0)
    IN2.value(0)

def ramp_to(start, end, step=5, delay_ms=100):
    # Limitar rangos entre 0 y 100 por seguridad
    start = max(0, min(100, start))
    end = max(0, min(100, end))

    if start <= end:
        for speed in range(start, end + 1, step):
            set_speed(speed)
            print("Velocidad:", speed, "%")
            sleep_ms(delay_ms)
    else:
        for speed in range(start, end - 1, -step):
            set_speed(speed)
            print("Velocidad:", speed, "%")
            sleep_ms(delay_ms)
            
    # asegurar que quede exactamente en el valor final
    set_speed(end)


stop()
sleep_ms(500)
print("Inicio")


while True:
    # 1. Botón FORWARD 
    if btn_fwd.value() == 0:
        if estado != "FORWARD":
            # Si iba en reversa, primero desacelerar a 0% por seguridad
            if estado == "REVERSE" and vel_actual > 0:
                print("Cambiando dirección: bajando a 0%...")
                ramp_to(vel_actual, 0)
                sleep_ms(200)
            
            print("Giro: FORWARD")
            forward()
            ramp_to(0, 100)
            estado = "FORWARD"

    # 2. Botón REVERSE
    elif btn_rev.value() == 0:
        if estado != "REVERSE":
            # Si iba hacia adelante, primero desacelerar a 0% por seguridad
            if estado == "FORWARD" and vel_actual > 0:
                print("Cambiando dirección: bajando a 0%...")
                ramp_to(vel_actual, 0)
                sleep_ms(200)
            
            print("Giro: REVERSE")
            reverse()
            ramp_to(0, 75)  
            estado = "REVERSE"

    # 3. Botón STOP
    elif btn_stop.value() == 0:
        if estado != "STOP":
            print("Deteniendo con rampa...")
            ramp_to(vel_actual, 0)
            stop()
            estado = "STOP"
            print("Motor en STOP")

    sleep_ms(20) 
