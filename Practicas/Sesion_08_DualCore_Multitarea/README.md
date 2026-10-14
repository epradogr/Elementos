## DualCore Multitarea
En esta práctica se lleva a cabo la programación de multihilos para llevar el procesamiento de nuestra raspberry a otro nivel. Se programa utilizando la librería threads y se elabora un sistema multitarea donde una tarea monitorea un sensor analógico a alta velocidad y otras tareas actualizan interfaz, terminal y botón sin bloquear el programa. También se incluye una versión similar en Wokwi pero sustituyendo threads por ticks para hacer un scheduler.

## Tabla de Pruebas Obligatoria

| Prueba | Resultado esperado | PASS/FAIL |
|---|---|---|
| Potenciómetro bajo | NORMAL / LED verde | |
| Potenciómetro medio | WARNING / LED amarillo | |
| Potenciómetro alto | ALARM / rojo parpadea | |
| Botón fuera de ALARM | No reconoce alarma | |
| Botón durante ALARM | ACK=True / rojo fijo | |
| Salir de ALARM | ACK vuelve a False | |
| Heartbeat | LED azul cambia sin congelarse | |
| Serial | Muestra datos cada segundo | |
| Sensor a 20 ms | ~50 muestras por segundo | |
| Filtro | Reduce variaciones rápidas | |
| Pico física | `_thread` mantiene adquisición y UI | |
