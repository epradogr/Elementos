## DualCore Multitarea
En esta práctica se lleva a cabo la programación de multihilos para llevar el procesamiento de nuestra raspberry a otro nivel. Se programa utilizando la librería threads y se elabora un sistema multitarea donde una tarea monitorea un sensor analógico a alta velocidad y otras tareas actualizan interfaz, terminal y botón sin bloquear el programa. También se incluye una versión similar en Wokwi pero sustituyendo threads por ticks para hacer un scheduler.

## Tabla de Pruebas Obligatoria

| Prueba | Resultado esperado | DO 08 COMPLETO (Mono-core) | SHOW 2 MEJORADO (Dual-core `_thread`) | Observaciones |
| :--- | :--- | :---: | :---: | :--- |
| **Potenciómetro bajo** | NORMAL / LED verde | PASS | PASS | Pin 13 ON, pines 14 y 15 OFF cuando `percent < 50%`. |
| **Potenciómetro medio** | WARNING / LED amarillo | PASS | PASS | Pin 14 ON, pines 13 y 15 OFF cuando `50% <= percent < 75%`. |
| **Potenciómetro alto** | ALARM / LED rojo parpadea | PASS | PASS | Pin 15 conmuta a 2.5 Hz cuando `percent >= 75%` y `ack == False`. |
| **Botón fuera de ALARM** | No reconoce alarma | PASS | PASS | Pulsar en NORMAL o WARNING emite mensaje y no altera la bandera ACK. |
| **Botón durante ALARM** | ACK=True / LED rojo fijo | PASS | PASS | Cambia `ack = True`, el parpadeo cesa y Pin 15 queda encendido continuo. |
| **Salir de ALARM** | ACK vuelve a False | PASS | PASS | Al descender de 75%, `ack` se limpia automáticamente para la siguiente alarma. |
| **Heartbeat** | LED conmuta sin congelarse | PASS | PASS | Pin 12 alterna periódicamente a 5 Hz (cada 200 ms) confirmando que Core 0 no se bloquea. |
| **Serial** | Muestra datos cada segundo | PASS | PASS | La tarea de logging imprime telemetría por consola UART/USB a 1 Hz (`log_period = 1000`). |
| **Sensor a 20 ms** | ~50 muestras por segundo | PASS | PASS | Muestreo continuo a 50 Hz sin pausas prolongadas. |
| **Filtro** | Reduce variaciones rápidas | PASS | FAIL | SHOW 2 omitió el buffer FIFO de 8 muestras; clasifica directo con `raw_value`. |
| **Pico física** | `_thread` mantiene adquisición y UI | N/A | PASS | Distribución de carga por hardware: Core 1 adquiere y Core 0 atiende UI/Botón con `lock`. |
