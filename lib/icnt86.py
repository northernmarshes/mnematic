# *****************************************************************************
# * | File        :	  Pico_CapTouch_ePaper_Test_2in9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-02
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, I2C
import utime


# TP
TRST = 16
INT = 17


class config:
    def __init__(self, i2c_addr):
        self.trst_pin = Pin(TRST, Pin.OUT)
        self.int_pin = Pin(INT, Pin.IN)

        self.address = i2c_addr
        self.i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def i2c_writebyte(self, reg, value):
        wbuf = [(reg >> 8) & 0xFF, reg & 0xFF, value]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_write(self, reg):
        wbuf = [(reg >> 8) & 0xFF, reg & 0xFF]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_readbyte(self, reg, len):
        self.i2c_write(reg)
        rbuf = bytearray(len)
        self.i2c.readfrom_into(self.address, rbuf)
        return rbuf

    def module_exit(self):
        self.digital_write(self.trst_pin, 0)


class ICNT_Development:
    def __init__(self):
        self.Touch = 0
        self.TouchGestureid = 0
        self.TouchCount = 0

        self.TouchEvenid = [0, 1, 2, 3, 4]
        self.X = [0, 1, 2, 3, 4]
        self.Y = [0, 1, 2, 3, 4]
        self.P = [0, 1, 2, 3, 4]


class ICNT86:
    def __init__(self):
        self.config = config(0x48)

    def ICNT_Reset(self):
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 0)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)

    def ICNT_Write(self, Reg, Data):
        self.config.i2c_writebyte(Reg, Data)

    def ICNT_Read(self, Reg, len):
        return self.config.i2c_readbyte(Reg, len)

    def ICNT_ReadVersion(self):
        buf = self.ICNT_Read(0x000A, 4)
        print(buf)

    def ICNT_Init(self):
        self.ICNT_Reset()
        self.ICNT_ReadVersion()

    def ICNT_Scan(self, ICNT_Dev, ICNT_Old):
        buf = []
        mask = 0x00

        if ICNT_Dev.Touch == 1:
            ICNT_Dev.Touch = 0
            buf = self.ICNT_Read(0x1001, 1)

            if buf[0] == 0x00:
                self.ICNT_Write(0x1001, mask)
                self.config.delay_ms(1)
                # print("buffers status is 0")
                return
            else:
                ICNT_Dev.TouchCount = buf[0]

                if ICNT_Dev.TouchCount > 5 or ICNT_Dev.TouchCount < 1:
                    self.ICNT_Write(0x1001, mask)
                    ICNT_Dev.TouchCount = 0
                    # print("TouchCount number is wrong")
                    return

                buf = self.ICNT_Read(0x1002, ICNT_Dev.TouchCount * 7)
                self.ICNT_Write(0x1001, mask)

                ICNT_Old.X[0] = ICNT_Dev.X[0]
                ICNT_Old.Y[0] = ICNT_Dev.Y[0]
                ICNT_Old.P[0] = ICNT_Dev.P[0]

                for i in range(0, ICNT_Dev.TouchCount, 1):
                    ICNT_Dev.TouchEvenid[i] = buf[6 + 7 * i]
                    # ICNT_Dev.X[i] = ((buf[2 + 7*i] << 8) + buf[1 + 7*i])
                    # ICNT_Dev.Y[i] = ((buf[4 + 7*i] << 8) + buf[3 + 7*i])
                    ICNT_Dev.X[i] = 127 - ((buf[4 + 7 * i] << 8) + buf[3 + 7 * i])
                    ICNT_Dev.Y[i] = (buf[2 + 7 * i] << 8) + buf[1 + 7 * i]
                    ICNT_Dev.P[i] = buf[5 + 7 * i]

                print(ICNT_Dev.X[0], ICNT_Dev.Y[0], ICNT_Dev.P[0])
                return
        return
