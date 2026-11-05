## Sesion 10 Smart I2C
Practica realizada por Eduardo Prado y Andrea Ceja

**Objetivo**: Implementar un monitor HMI inteligente basado en MicroPython utilizando el protocolo I2C con tres pantallas interactivas, un canal ADC para lectura analógica, control por botón y un indicador LED de alarma.

**Pines**: 
* **SDA**: GP4
* **SCL**: GP5
* **ADC (Entrada analógica)**: GP26
* **Botón de cambio de página**: GP16 (con resistencia interna PULL_UP)
* **LED de Alarma**: GP15
* **Frecuencia I2C**: 400,000 Hz
  
Imagen de esquemático de Wokwi:

<img width="513" height="452" alt="image" src="https://github.com/user-attachments/assets/4adbce14-bcb6-48a9-ab41-0aca4945d71f" />

**Resultados de i2c.scan()**:
* **Dirección I2C de la OLED**: 0x3C
* **Resultado del escaneo en Hexadecimal**: 0x3c
* **Resultado del escaneo en Decimal**: 60

**¿Por qué varios disppositivos pueden compartir SDA/SCL?**

Se pueden compartir varios dispositivos ya que su arquitectura de dirección por hardware de 7 bits y esquema de colector abierto con resistencias de pull-up permite que cada dispositivo conectado posea una dirección única, lo que permite al microcontrolador comunicarse de forma selectiva con un dispositivo a la vez sin interferencias en el bus.

**Evidencia**

<img width="1366" height="768" alt="imagen (1)" src="https://github.com/user-attachments/assets/c17d51e0-dab3-490e-8972-ff52b1504ff6" />



### Tabla de resultados
| Prueba | Resultado esperado | PASS/FAIL | Evidencia |
|---|---|---|---|
| Scan I2C | OLED detectada (normalmente 0x3C) | **PASS** | Mensaje en consola de `i2c.scan()` exitoso |
| LIVE < 50% | NORMAL | **PASS** | Visualización en página 1 de la OLED |
| LIVE 50-74.9% | WARNING | **PASS** | Visualización en página 1 de la OLED |
| LIVE >= 75% | ALARM + LED ON | **PASS** | Encendido de LED en GP15 y estado en pantalla |
| Boton 1 vez | Cambia una pagina | **PASS** | Transición al presionar el botón en GP16 |
| Ciclo de boton | LIVE -> I2C -> STATS -> LIVE | **PASS** | Rotación correcta de las 3 pantallas |
| I2C page | Muestra direccion(es) detectadas | **PASS** | Despliegue de direcciones en la página 2 |
| STATS | min/max/samples cambian | **PASS** | Actualización de contadores en página 3 |
| Desconectar OLED (diagnostico) | Scan no muestra 0x3C / mensaje claro | **PASS** | Alerta de advertencia impresa en consola al fallar el escaneo |
