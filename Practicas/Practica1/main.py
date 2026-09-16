from machine import Pin # Biblioteca para declarar mis pines
from time import sleep_ms # Biblioteca para sleep

#Pines GPIO de mi rasp
CAR_RED = 15
CAR_YELLOW = 14
CAR_GREEN = 13
PED_RED = 12
PED_GREEN = 11
BUTTON = 16

#Declaración de la función del pin IN/OUT
car_red = Pin(CAR_RED, Pin.OUT)
car_yellow = Pin(CAR_YELLOW, Pin.OUT)
car_green = Pin(CAR_GREEN, Pin.OUT)
ped_red = Pin(PED_RED, Pin.OUT)
ped_green = Pin(PED_GREEN, Pin.OUT)
button = Pin(BUTTON, Pin.IN, Pin.PULL_UP) # PULL UP, empieza en 1, al presionar 0

# Definir mis parámetros para poder utilizarlos en las funciones
def set_lights(car_r, car_y, car_g, ped_r, ped_g):
    car_red.value(car_r)
    car_yellow.value(car_y)
    car_green.value(car_g)
    ped_red.value(ped_r)
    ped_green.value(ped_g)
# Declaración de estados: indicará que luces estarán encendidas
# y el orden va acorde a mi función set lights, así para cada estado

def cars_go():
    print("S0 REPOSO: Autos pasan, peaton espera")
    set_lights(0,0,1,1,0)

def cars_prepare_stop():
    print("S1 Trancision: autos preparando alto")
    set_lights(0,1,0,1,0)

def pedestrians_go():
    print("S2 CRUCE: peaton puede cruzar")
    set_lights(1,0,0,0,1)

def pedestrians_finish():
    print("S3: FIN CRUCE: peaton verde parpadea")
    set_lights(1,0,0,0,1)
    for _ in range(6):
        ped_green.toggle() # Toggle registra el valor anterior y lo cambia con un XOR
        sleep_ms(300)
        ped_green.value(0) #Se asigna manualmente el valor
        ped_red.value(1)

# secuencia de luces
def crossing_sequence():
    cars_prepare_stop()
    sleep_ms(1500)

    pedestrians_go()
    sleep_ms(4000)

    pedestrians_finish()
    sleep_ms(500)

    cars_go()

# el default
cars_go()
last=1

while True:
    now = button.value() # nuevo valor del botón

    if last == 1 and now == 0:
        sleep_ms(30) #Antirrebote
        
        if button.value() == 0: # Al presionar el botón
            print("Peticion peatonal!")
            crossing_sequence()

            while button.value() == 0: #Evita que la secuencia se itere una y otra vez
                sleep_ms(10)
    last = now # guarda el valor del botón
    sleep_ms(10)
