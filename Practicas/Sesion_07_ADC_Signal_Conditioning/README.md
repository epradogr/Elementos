## Práctica 7 ADC Signal
Lo que se logró en esta práctica fue acer un sistema de monitoreo de señales analógicas usando los pines ADC (convertidor analógico a digital) para poder leer sensores, eneste caso potenciometro y fotorresistor. Para esto nos llegará la señal raw que es el número de variaciones eléctricas que con una regla de tres pasaremos a porcentaje y a voltaje para poder hacer una medición correcta. 
Para evitar ruido se matnntiene una ventana con la función de suavizar la señal y estabilizar el sistema. 
Finalmente, el programa toma el porcentaje de señal que obtuvimos y lo compara con diferentes parámetros que hayamos puestos para saber si se encuentra en un nivel NORMAL, WARNING o ALARM.
