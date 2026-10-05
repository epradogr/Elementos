## Práctica 7 ADC Signal
Lo que se logró en esta práctica fue hacer un sistema de monitoreo de señales analógicas usando los pines ADC (convertidor analógico a digital) para poder leer sensores, en este caso potenciometro y fotorresistor.

Para esto nos llegará la señal raw que es el número de variaciones eléctricas y, con una regla de tres se calculará el porcentaje y el voltaje para poder adecuar nuestras mediciones.
Para evitar ruido se matnntiene una ventana con la función de suavizar la señal y estabilizar el sistema. 

Finalmente, el programa toma el porcentaje de señal que obtuvimos y lo compara con diferentes parámetros que hayamos puestos para saber si se encuentra en un nivel NORMAL, WARNING o ALARM.

## Tabla de pruebas
| Prueba | Resultado esperado | PASS/FAIL |
|---|---|---|
| ADC mínimo | raw cercano a 0 / 0 % | PASS |
| ADC medio | raw cercano a 32767 / 50 % | PASS |
| ADC máximo | raw cercano a 65535 / 100 % | PASS |
| Filtro | la señal filtrada cambia suavemente | PASS |
| Normal | LED verde activo | PASS |
| Warning | LED amarillo activo | PASS |
| Alarm | LED rojo activo | PASS |
| Recuperación | vuelve de ALARM a NORMAL al bajar señal | PASS |
