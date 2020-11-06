from machine import I2C, Pin
from micropython import const
import ht16k33_matrix
import framebuf
from gfx import GFX
import math

_HT16K33_BLINK_CMD = const(0x80)
_HT16K33_BLINK_DISPLAYON = const(0x01)
_HT16K33_CMD_BRIGHTNESS = const(0xE0)
_HT16K33_OSCILATOR_ON = const(0x21)

_HT16K33_KEYS_REGISTER =  const(0x40)
_HT16K33_KEYINT_REGISTER = const(0x60)
_HT16K33_ADDRESS = const(0x70)


class Matrix5x5(ht16k33_matrix.HT16K33Matrix):
    WIDTH = 5
    HEIGHT = 5
    FORMAT = framebuf.MONO_HMSB
    FB_BPP = 1

    def _copy_buf(self):
        for y in range(5):
            b = self._fb_buffer[y]
            self.buffer[y * 2] = (b >> 1) | (b << 4)

    def drawPixel(self, x, y):
        if x == 0:
            self.pixel(1, y, True)
        elif x == 4:
            self.pixel(0,y, True)
        else:
            self.pixel(x+1, y, True)



class modGFX(GFX):

    def half_circle(self, x0, y0, radius, *args, **kwargs):
        # Circle drawing function.  Will draw a single pixel wide circle with
        # center at x0, y0 and the specified radius.
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        self._pixel(x0, y0 + radius, *args, **kwargs)
        self._pixel(x0, y0 - radius, *args, **kwargs)
        self._pixel(x0 + radius, y0, *args, **kwargs)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self._pixel(x0 + x, y0 + y, *args, **kwargs)
            self._pixel(x0 + x, y0 - y, *args, **kwargs)



    def draw_A(self, x0, y0, x1, y1):
        self.line( x0, y0, x1, y1)
        self.line( x1, y1, x0+4, y0)
        y3 = math.ceil(max(y1,y0)/2)
        x3 = math.ceil(max(x1,x0)/2)
        y4 = math.ceil(max(y0,y1)/2)
        x4 = math.ceil(max(x1, x0+4)/2)
        self.line( x3, y3, x4, y4)

    def draw_B(self, x0, y0, y1):
        self.line(x0,y0, x0, y1)
        y3 = y1+1//4
        y4 = 3*y3
        self.half_circle(x0+1,y3,y3)
        self.half_circle(x0+1,3,1)
        




i2c = I2C(sda=Pin(4), scl=Pin(5))

display = Matrix5x5(i2c)

display.fill(0)
graphics = modGFX(5, 5, display.drawPixel)
graphics.draw_A(0,0,2,4)
display.show()