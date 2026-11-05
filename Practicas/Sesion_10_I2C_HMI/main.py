# SESION 10  Andrea Ceja y Eduardo Prado
# Monitor HMI: ADC + OLED SSD1306 por I2C (con modo consola si no hay OLED)
 
from machine import Pin, I2C, ADC
from time import sleep_ms
 
# Configuración de pines e I2C
SDA_PIN = 4
SCL_PIN = 5
OLED_ADDR = 0x3C
 
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400_000)
 
# Validación de dispositivos I2C al iniciar
devices = i2c.scan()
print('Dispositivos I2C detectados (hex):', [hex(x) for x in devices])
print('Dispositivos I2C detectados (dec):', devices)
 
HAS_OLED = OLED_ADDR in devices
 
if HAS_OLED:
    print('OLED detectada correctamente en la direccion 0x3C.')
else:
    print('ADVERTENCIA: OLED no encontrada en 0x3C.')
 
 
class ConsoleOLED:
    """Pantalla falsa: guarda el texto para imprimirlo en la consola."""
    def __init__(self):
        self.lines = []
 
    def fill(self, c):
        self.lines = []
 
    def text(self, s, x, y, c=1):
        self.lines.append((y, s))
 
    def rect(self, *a):
        pass
 
    def fill_rect(self, *a):
        pass
 
    def show(self):
        pass
 
 
if HAS_OLED:
    from ssd1306 import SSD1306_I2C
    oled = SSD1306_I2C(128, 64, i2c, addr=OLED_ADDR)
else:
    oled = ConsoleOLED()
    print('Modo consola: sin OLED, se imprime en el Shell.')
 
adc = ADC(26)
button = Pin(16, Pin.IN, Pin.PULL_UP)
led_alarm = Pin(15, Pin.OUT)
 
page = 0
last_button = 1
samples = 0
min_value = 100.0
max_value = 0.0
tick = 0
 
 
def classify(p):
    if p < 50:
        return 'NORMAL'
    elif p < 75:
        return 'WARNING'
    else:
        return 'ALARM'
 
 
def live_screen(p, state):
    oled.text('PAGE 1 - LIVE', 0, 0)
    oled.text('ADC {:5.1f}%'.format(p), 0, 18)
    oled.text(state, 0, 34)
    # Barra de progreso proporcional
    oled.rect(4, 50, 120, 10, 1)
    fill_w = int(116 * p / 100)
    if fill_w > 116:
        fill_w = 116
    oled.fill_rect(6, 52, fill_w, 6, 1)
 
 
def bus_screen():
    oled.text('PAGE 2 - I2C', 0, 0)
    oled.text('SDA: GP{}'.format(SDA_PIN), 0, 17)
    oled.text('SCL: GP{}'.format(SCL_PIN), 0, 29)
    dev_str = ','.join(hex(x) for x in devices)
    oled.text('DEV:' + dev_str, 0, 43)
 
 
def stats_screen():
    oled.text('PAGE 3 - STATS', 0, 0)
    oled.text('MIN:{:5.1f}%'.format(min_value), 0, 17)
    oled.text('MAX:{:5.1f}%'.format(max_value), 0, 29)
    oled.text('N:{}'.format(samples), 0, 43)
 
 
print('Monitor HMI iniciado correctamente.')
 
while True:
    raw = adc.read_u16()
    percent = raw * 100 / 65535
    state = classify(percent)
 
    samples += 1
    min_value = min(min_value, percent)
    max_value = max(max_value, percent)
 
    # El LED de alarma se enciende únicamente en estado ALARM
    led_alarm.value(state == 'ALARM')
 
    # Flanco de bajada del botón para cambiar de página
    current = button.value()
    if last_button == 1 and current == 0:
        page = (page + 1) % 3
        print('Cambio a PAGE', page + 1)
    last_button = current
 
    # Limpiar, dibujar la página activa y actualizar el display
    oled.fill(0)
    if page == 0:
        live_screen(percent, state)
    elif page == 1:
        bus_screen()
    else:
        stats_screen()
    oled.show()
 
    # Sin OLED: imprimir en el Shell cada 0.5 s
    if not HAS_OLED:
        tick += 1
        if tick % 5 == 0:
            print(' | '.join(s for y, s in sorted(oled.lines)),
                  '#' * int(percent / 5))
 
    sleep_ms(100)
