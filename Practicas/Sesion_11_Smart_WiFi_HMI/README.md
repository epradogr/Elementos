



## Tabla de pruebas

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

*
