from icnt86 import ICNT86, ICNT_Development
import utime

tp = ICNT86()
dev = ICNT_Development()
old = ICNT_Development()

tp.ICNT_Init()

while True:
    dev.Touch = 1
    tp.ICNT_Scan(dev, old)
    utime.sleep_ms(50)
