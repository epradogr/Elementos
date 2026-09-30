## Práctica 6 PWM
En esta práctica se hizo uso de Pulse Width Modulation, que sirve para encender y apagar muy rápido para controlar energía promedio, cambiando el tiempo que la salida permanece encendida. Con la Raspberry lo conectamos a un puente H para poder demostrar su funcionamiento con un motor y junto con la Raspberry poder controlarlo, ya sea que vaya de reversa, hacia en frente o que frene, todo con aceleración en rampa. Para llevar a cabo esta cráctica usamos conceptos como:

### Duty cycle
Es el porcentaje de tiempo durante un período completo en el cual la señal PWM permanece en estado alto. Al variar el ciclo de trabajo de 0% a 100%, se modula la potencia promedio entregada al motor.
### IN1/IN2
Son las entradas lógicas del puente H van a controar lo que hace nuestro motor, dependiendo si están recibiendo una señal en alto o en bajo, controlan la dirección del motor o incluso si se detiene, aquí es donde la raspberry y los botónes se comunican con el puente H y con el motor.
### ENA 
Es la entrada Enable del puente H y sirve para conectarse con PWM a la rasp, así determina que tan rápido va nuestro motor.
### Uso de rampa
Se usa una rampa la cuál es un algoritmo por software con la función de ir progresando uniformemente la velocidad para evitar esfuerzo mecánico y evitar variaciones bruscas de corriente.
### ¿Por qué no invertimos dirección a alta velocidad? 
Porque el pico de energía que se necesita para que alcance una alta velocidad es basante alto, si se invierte al instante se está forzando que el motor gire hacia la dirección contraria lo cuál tomará mucha más corriente, que provocará calentamiento y esfuerzo mecánico, algo que puede causar que se dañen nuestros componentes, por eso es mejor hacer una desaseleración de seguridad; siempre que se quiera invertir la dirección desacelerar primero para evitar problemas.

### Tabla de Pruebas

| Prueba (Test) | Comportamiento Esperado | Resultado |
| :--- | :--- | :---: |
| **STOP** | Motor detenido por completo (0% PWM) | PASS |
| **FORWARD** | Giro horario progresivo hacia adelante | PASS |
| **REVERSE** | Giro antihorario progresivo en reversa | PASS |
| **25/50/75/100%** | Escalones de velocidad claramente diferenciados | PASS |
| **Ramp UP** | Incremento progresivo de velocidad sin tirones | PASS |
| **Ramp DOWN** | Reducción progresiva de velocidad al detener o cambiar sentido | PASS |
| **Cambio dirección** | Desacelera primero a 0% antes de conmutar sentido | PASS |
### Problemas encontrados
El único problema que tuve fue que el código en Thonny funcionaba pero físicamente había corto circuitos en mi puente H.
También que fue difícil medir el momento exacto con el multímetro en el que la velocidad llegaba a cada espacio de la tabla.
