from machine import Pin, SPI
from utime import sleep
from lib.ds1302 import DS1302
import framebuf
from Pico_ePaper_2_9 import EPD_2in9_Landscape


def main():
    app = Mnematic()
    app.main()


class Mnematic(EPD_2in9_Landscape):
    def __init__(self):
        super().__init__()
        # Pinout
        self.buzz = Pin(22, Pin.OUT)
        self.rtc = DS1302(Pin(18), Pin(19), Pin(20))

        # Screen size
        self.HEIGHT = 128
        self.WIDTH = 296
        self.PADDING = 5

        # Initialisation
        self.rtc.start()
        self.epd = EPD_2in9_Landscape()
        print("init function runs")
        self.epd.Clear(0xFF)

    def main(self):
        try:
            print("hello!")
            self.epd.fill(0xFF)

            print("status function runs")

            # Draw left panel
            self.epd.rect(
                self.PADDING,
                self.PADDING,
                self.WIDTH // 2 - 2 * self.PADDING,
                self.HEIGHT - 2 * self.PADDING,
                0x00,
            )
            self.epd.text("Hello", 10, 60, 0x00)

            # Draw right panel
            t = self.rtc.date_time()
            self.epd.rect(
                self.WIDTH // 2 + self.PADDING,
                self.PADDING,
                self.WIDTH // 2 - 2 * self.PADDING,
                self.HEIGHT - 2 * self.PADDING,
                0x00,
            )
            self.epd.text(f"{t[2]:02d}|{t[1]:02d}", 178, 60, 0x00)
            self.epd.text(f" {t[0]}", 178, 70, 0x00)

            # Display buffer
            self.epd.display(self.epd.buffer)
        except Exception as e:
            print(f"Error: {e}")

    def buzzer(self):
        # Set frequency
        self.buzz.freq(200)

        # Set strengh
        self.buzz.duty_u16(1000)
        sleep(2)

        # Turn off buzzer
        self.buzz.duty_u16(0)


if __name__ == "__main__":
    main()
