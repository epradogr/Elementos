## Práctica 7 ADC Signal
Lo que se logró en esta práctica fue hacer un sistema de monitoreo de señales analógicas usando los pines ADC (convertidor analógico a digital) para poder leer sensores, en este caso potenciometro y fotorresistor.

Para esto nos llegará la señal raw que es el número de variaciones eléctricas y, con una regla de tres se calculará el porcentaje y el voltaje para poder adecuar nuestras mediciones.
Para evitar ruido se matnntiene una ventana con la función de suavizar la señal y estabilizar el sistema. 

Finalmente, el programa toma el porcentaje de señal que obtuvimos y lo compara con diferentes parámetros que hayamos puestos para saber si se encuentra en un nivel NORMAL, WARNING o ALARM.
