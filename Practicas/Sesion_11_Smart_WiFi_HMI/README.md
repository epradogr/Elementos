## Smart WiFi HMI
Práctica realizada por Eduardo Prado y Andrea Ceja.

La práctica consistió en hacer una conexión WiFi entre la laptop y la rasp pi pico 2 W. Esto para poder modificar valores y realizar tareas vía red inalámbrica. En este caso diseñamos un dashboard que controlara dos leds, uno con pwm y otro con toggle. A parte de que se viera en el dashboard también aparece en un OLED. Para la práctica se sugería el uso de un ssd1306, pero al no poder conseguirlo, ocupamos un st7735s, los únicos cambios fueron las librerías y una sección del códgo. Al ingresar el servidor se toman en cuenta URL HTTP tales como api/status y /api/value; también errores como 400 valor incorrecto y 404 not found.


## Explicación del funcionamiento

### 1. ¿Qué significa STA?
STA (Station Mode) es el modo en el que la Raspberry Pi Pico se conecta a una red Wi-Fi existente para obtener una dirección IP y comunicarse con otros dispositivos.

### 2. ¿Qué hacen `bind()`, `listen()` y `accept()`?
- bind(): Asocia el servidor a una dirección IP y un puerto, en este caso el puerto 80 de HTTP.
- listen(): Pone al servidor en espera de conexiones entrantes.
- accept(): Acepta una conexión de un cliente, como un navegador web.

### 3. ¿Cómo se transforma 0–100 % a `duty_u16()`?
La función duty_u16() utiliza valores entre 0 y 65535 para controlar el PWM.

Se utiliza la fórmula:

duty = int(porcentaje * 65535 / 100)

Por ejemplo, un 50 % corresponde aprox a 32768. Así se controla el brillo del LED conectado a GP15.

### 4. ¿Qué hace el slider HTML?
El slider permite seleccionar un porcentaje entre 0 y 100 para controlar el brillo del LED. Al soltarlo, envía el valor seleccionado a la Raspberry Pi Pico mediante una petición HTTP.

### 5. ¿Por qué se usa `fetch()`?
Se utiliza fetch() en JavaScript para enviar peticiones HTTP al servidor de la Pico y recibir respuestas JSON, permitiendo actualizar el estado de los LEDs sin recargar toda la página.

### 6. ¿Qué diferencia existe entre HTML y JSON?
HTML se utiliza para estructurar y mostrar la interfaz web, incluyendo botones, textos y controles.

JSON es un formato de intercambio de datos que permite comunicar valores como el PWM, el estado del LED2, la dirección IP y el número de peticiones.

### 7. ¿Cómo se integra I2C/OLED con el servidor web?
En el proyecto original, la pantalla OLED SSD1306 utiliza I2C para mostrar la información del sistema. En nuestra implementación se utilizó una pantalla TFT ST7735S con comunicación SPI en lugar de I2C. El servidor web recibe las peticiones HTTP, actualiza las variables del sistema y posteriormente actualiza la pantalla para mostrar la IP, el porcentaje PWM, el estado del LED2 y el contador de peticiones.




### Tabla de pruebas

| Prueba | Resultado |
|---|---|
| Abrir `/` — Dashboard visible | PASS |
| Slider = 0 — LED PWM apagado | PASS |
| Slider = 37 — Brillo intermedio | PASS |
| Slider = 100 — Brillo máximo | PASS |
| TOGGLE LED 2 — GP14 cambia ON/OFF | PASS |
| OLED/TFT — Refleja PWM y LED2 | PASS |
| `/api/status` — JSON correcto | PASS |
| `/api/pwm?value=150` — Error 400 | PASS |
| `/ruta-que-no-existe` — Error 404 | PASS |
