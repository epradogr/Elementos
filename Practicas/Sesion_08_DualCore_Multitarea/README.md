## DualCore Multitarea
En esta práctica se lleva a cabo la programación de multihilos para llevar el procesamiento de nuestra raspberry a otro nivel. Se programa utilizando la librería threads y se elabora un sistema multitarea donde una tarea monitorea un sensor analógico a alta velocidad y otras tareas actualizan interfaz, terminal y botón sin bloquear el programa. También se incluye una versión similar en Wokwi pero sustituyendo threads por ticks para hacer un scheduler.

## Tabla de Pruebas Obligatoria

| Prueba | Resultado esperado | PASS/FAIL |
|---|---|---|
| Potenciómetro bajo | NORMAL / LED verde | PASS |
| Potenciómetro medio | WARNING / LED amarillo | PASS |
| Potenciómetro alto | ALARM / rojo parpadea | PASS |
| Botón fuera de ALARM | No reconoce alarma | PASS |
| Botón durante ALARM | ACK=True / rojo fijo | PASS |
| Salir de ALARM | ACK vuelve a False | PASS |
| Heartbeat | LED azul cambia sin congelarse | PASS |
| Serial | Muestra datos cada segundo | PASS |
| Sensor a 20 ms | ~50 muestras por segundo | PASS |
| Filtro | Reduce variaciones rápidas | PASS |
| Pico física | `_thread` mantiene adquisición y UI | PASS |

## Preguntas de análisis

1. ¿Cuál es la diferencia entre multitarea cooperativa en Wokwi y dual-core real?
   Que en el dual core se están ocupando dos núcleos distintos del procesador lo cuál hace que las tareas y el procesamiento sean m´´as fluidos, en multitarea cooperativa esto no sucede porque se hace dentro de un solo núcleo pero aún así el sistema está optimizado para ser eficiente en el procesamiento.
3. ¿Por qué no usamos `sleep_ms(1000)` dentro de la tarea crítica del sensor?
 Porque sleep ms bloque todo el sistema lo cuál detiene cualquier proceso y retrocede y puede llegar a desfazar los procesos
5. ¿Por qué una tarea puede ejecutarse cada 20 ms y el terminal cada 1000 ms?
   no se
7. ¿Por qué se necesita `lock` cuando dos núcleos comparten datos?
   para que si se están tomando los mismos datos no llegue a haber un error en el sistema
9. ¿Qué diferencia hay entre **reconocer una alarma** y **eliminar la condición de alarma**?
10. ¿Qué evidencia demuestra que el sistema no se bloquea?
