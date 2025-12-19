from machine import Pin, SPI
import time
import json

from Pico_ePaper_2_9 import EPD_2in9_Portrait

epd = EPD_2in9_Portrait()
epd.init()
buzz = Pin(15, Pin.OUT)


def status():
    pass


def buzzer():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
