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

En la multitarea cooperativa las tareas se intercalan compartiendo el tiempo de CPU mediante ticks_ms. Cada tarea debe ejecutarse rápido y ceder voluntariamente el control para no congelar a las demás. En dual-core real dos líneas de ejecución corren al mismo tiempo de forma independiente (Core 1 muestrea el sensor mientras Core 0 gestiona la interfaz y el botón), evitando que el bloqueo de un núcleo afecte físicamente al otro.
   
2. ¿Por qué no usamos `sleep_ms(1000)` dentro de la tarea crítica del sensor?

Porque sleep_ms() detiene el ciclo de instrucción de la CPU durante ese intervalo.Congela por completo la detección del botón, el parpadeo de los LEDs y el heartbeat, provocando una pérdida de muestras y eliminando la capacidad de respuesta en tiempo real del sistema.


3. ¿Por qué una tarea puede ejecutarse cada 20 ms y el terminal cada 1000 ms?

Porque el sistema utiliza un multi-rate scheduler basado en marcas de tiempo independientes next_sensor y next_log.
En cada vuelta del bucle principal, se compara el tiempo actual ticks_ms() contra el objetivo de cada tarea mediante ticks_diff(). Como ninguna tarea se queda esperando a la otra ni bloquea el procesador, cada función se realiza cuando el sensor corre a 50 Hz(para capturar transiciones analógicas rápidas y la terminal a 1 Hz para no saturar el canal serial ni la CPU.

4. ¿Por qué se necesita `lock` cuando dos núcleos comparten datos?

Para evitar lecturas inconsistentes o corruptas. Si Core 0 intenta leer algo en lo que core 1 sigue trabajando, se leera algo inconsistente. El lock garantiza que solo un núcleo pueda acceder a la memoria a la vez, y el otro tiene que esperar a que este se desocupe, así se evitan inconsistencias.

   
5. ¿Qué diferencia hay entre **reconocer una alarma** y **eliminar la condición de alarma**?

Al reconocer una alarma el usuario se percata de esto y puede indicarle al sistema que se ha percatado, como en el caso de nuestra práctica que es presionar el botón, sin embargo, se sabe que hay una alarma pero esto no quita el estado de alarma. Eliminar la condición de alarma implica cambiar el estado que en primer lugar activa la alarma, en este caso cambiar el valor del potenciometro.

6. ¿Qué evidencia demuestra que el sistema no se bloquea?

El heartbeat que nunca deja de palpitar, el constante e incrementable muestreo y la respuesta inmediata del botón.
