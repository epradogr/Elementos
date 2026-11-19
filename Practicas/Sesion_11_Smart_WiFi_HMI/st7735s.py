"""Controlador MicroPython para TFT ST7735S 80x160 SPI.
Pensado para Raspberry Pi Pico W / Pico 2 W.
Utiliza framebuf.RGB565, sin dependencias externas.
"""
from machine import Pin
from time import sleep_ms
import framebuf


class ST7735S:
    WIDTH = 80
    HEIGHT = 160

    def __init__(self, spi, cs, dc, rst, x_offset=26, y_offset=1,
                 bgr=True, invert=True):
        self.spi = spi
        self.cs = cs if hasattr(cs, 'value') else Pin(cs, Pin.OUT)
        self.dc = dc if hasattr(dc, 'value') else Pin(dc, Pin.OUT)
        self.rst = rst if hasattr(rst, 'value') else Pin(rst, Pin.OUT)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.cs.value(1)
        self.dc.value(1)
        self.rst.value(1)
        self.buffer = bytearray(self.WIDTH * self.HEIGHT * 2)
        self.fb = framebuf.FrameBuffer(self.buffer, self.WIDTH,
                                       self.HEIGHT, framebuf.RGB565)
        self._txbuf = bytearray(512)
        self._reset()
        self._init(bgr, invert)
        self.fill(0)
        self.show()

    def _command(self, command, data=None):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytes((command,)))
        if data is not None:
            self.dc.value(1)
            self.spi.write(data)
        self.cs.value(1)

    def _reset(self):
        self.rst.value(1)
        sleep_ms(50)
        self.rst.value(0)
        sleep_ms(50)
        self.rst.value(1)
        sleep_ms(150)

    def _init(self, bgr, invert):
        self._command(0x01)  # SWRESET
        sleep_ms(150)
        self._command(0x11)  # SLPOUT
        sleep_ms(150)
        self._command(0xB1, b'\x01\x2c\x2d')
        self._command(0xB2, b'\x01\x2c\x2d')
        self._command(0xB3, b'\x01\x2c\x2d\x01\x2c\x2d')
        self._command(0xB4, b'\x07')
        self._command(0xC0, b'\xa2\x02\x84')
        self._command(0xC1, b'\xc5')
        self._command(0xC2, b'\x0a\x00')
        self._command(0xC3, b'\x8a\x2a')
        self._command(0xC4, b'\x8a\xee')
        self._command(0xC5, b'\x0e')
        self._command(0x3A, b'\x05')  # RGB565 16 bits
        self._command(0x36, bytes((0x08 if bgr else 0x00,)))
        self._command(0x21 if invert else 0x20)
        self._command(0x13)  # NORON
        sleep_ms(10)
        self._command(0x29)  # DISPON
        sleep_ms(100)

    def fill(self, color):
        self.fb.fill(color)

    def fill_rect(self, x, y, w, h, color):
        self.fb.fill_rect(x, y, w, h, color)

    def text(self, string, x, y, color):
        self.fb.text(string, x, y, color)

    def show(self):
        xs = self.x_offset
        ys = self.y_offset
        xe = xs + self.WIDTH - 1
        ye = ys + self.HEIGHT - 1
        self._command(0x2A, bytes((xs >> 8, xs & 255, xe >> 8, xe & 255)))
        self._command(0x2B, bytes((ys >> 8, ys & 255, ye >> 8, ye & 255)))
        self._command(0x2C)  # RAMWR
        self.cs.value(0)
        self.dc.value(1)
        # El framebuf de MicroPython almacena RGB565 en little-endian.
        # ST7735S recibe cada píxel en big-endian, así que intercambiamos bytes.
        buf = self.buffer
        tx = self._txbuf
        for start in range(0, len(buf), len(tx)):
            n = min(len(tx), len(buf) - start)
            for i in range(0, n, 2):
                tx[i] = buf[start + i + 1]
                tx[i + 1] = buf[start + i]
            self.spi.write(memoryview(tx)[:n])
        self.cs.value(1)
