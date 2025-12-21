from machine import Pin, SPI
import utime
from lib.ds1302 import DS1302
import framebuf
from Pico_ePaper_2_9 import EPD_2in9_Landscape
import json


def main():
    app = Mnematic()

    # Loop for constant work
    # while True:
    #     app.main()
    #     sleep(24*60*60)

    # One time init
    app.main()


class Mnematic(EPD_2in9_Landscape):
    def __init__(self):
        super().__init__()

        # Pinout
        self.buzz = Pin(22, Pin.OUT)
        self.rtc = DS1302(Pin(18), Pin(19), Pin(20))

        # Loading deadline from json
        data = {}
        try:
            with open("next_deadline.json", "r") as f:
                data = json.load(f)
        except OSError:
            print("File error")
        self.next_deadline = data["date"]

        # Sizing
        self.HEIGHT = 128
        self.WIDTH = 296
        self.FONTSIZE = 8
        self.PADDING = 5
        self.BAR = 30
        self.RECT_HEIGHT = self.HEIGHT - 2 * self.PADDING - self.BAR
        self.RECT_WIDTH = self.WIDTH // 2 - 2 * self.PADDING

        # Initialisation
        self.rtc.start()
        self.epd = EPD_2in9_Landscape()
        self.epd.Clear(0xFF)

        # Calculating time
        self.t = self.rtc.date_time()

        self.weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.day_num = self.t[3]
        self.weekday = self.weekdays[int(self.day_num) - 1]

        # Calculating time to deadline
        # Parsing json deadline
        parts = self.next_deadline.split("-")
        self.next_date = str(f"{parts[2]}/{parts[1]}")
        deadline_timestamp = utime.mktime(
            (int(parts[0]), int(parts[1]), int(parts[2]), 0, 0, 0, 0, 0)
        )
        # Parsing rtc time
        current_timestamp = utime.mktime(
            (self.t[0], self.t[1], self.t[2], 0, 0, 0, 0, 0)
        )

        self.days_left = (deadline_timestamp - current_timestamp) // 86400

        # Calculating percents

        self.percents = str(100 - (round((self.days_left / 30) * 100))) + " %"

        # Calculating progress bar width
        self.bar_percentage = 1 - (self.days_left / 30)
        self.BAR_FILLED = round((self.WIDTH - 2 * self.PADDING) * self.bar_percentage)

    def main(self):
        try:
            self.epd.fill(0xFF)

            # ----- Draw left panel -----
            self.epd.rect(
                self.PADDING,
                self.PADDING,
                self.RECT_WIDTH,
                self.RECT_HEIGHT,
                0x00,
            )
            self.epd.text(
                str(self.days_left),
                self.PADDING + self.RECT_WIDTH // 4,
                self.PADDING + self.RECT_HEIGHT // 2 - 10,
                0x00,
            )
            self.epd.text(
                "DAYS",
                self.PADDING + self.RECT_WIDTH // 2,
                self.PADDING + self.RECT_HEIGHT // 2 - 20,
                0x00,
            )
            self.epd.text(
                "LEFT",
                self.PADDING + self.RECT_WIDTH // 2,
                self.PADDING + self.RECT_HEIGHT // 2,
                0x00,
            )

            self.epd.text(
                f"Until {self.next_date}",
                self.PADDING + 25,
                self.PADDING + self.RECT_HEIGHT // 2 + 25,
                0x00,
            )

            # ----- Draw right panel -----
            self.epd.rect(
                self.WIDTH // 2 + self.PADDING,
                self.PADDING,
                self.RECT_WIDTH,
                self.RECT_HEIGHT,
                0x00,
            )
            # Weekday
            self.epd.text(
                self.weekday,
                self.PADDING * 3
                + self.RECT_WIDTH
                + self.RECT_WIDTH // 2
                - (len(self.weekday) * 8 // 2),
                self.PADDING + self.RECT_HEIGHT // 2 - 20,
                0x00,
            )

            # Day and month
            self.epd.text(
                f"{self.t[2]:02d}/{self.t[1]:02d}",
                self.PADDING * 3 + self.RECT_WIDTH + self.RECT_WIDTH // 2 - 20,
                self.PADDING + self.RECT_HEIGHT // 2,
                0x00,
            )

            # Year
            self.epd.text(
                f" {self.t[0]}",
                self.PADDING * 3 + self.RECT_WIDTH + self.RECT_WIDTH // 2 - 25,
                self.PADDING + self.RECT_HEIGHT // 2 + 20,
                0x00,
            )

            # ----- Draw progress bar -----
            self.epd.rect(
                self.PADDING,
                self.PADDING * 2 + self.RECT_HEIGHT,
                self.WIDTH - 2 * self.PADDING,
                self.BAR - self.PADDING,
                0x00,
            )
            self.epd.fill_rect(
                self.PADDING,
                self.PADDING * 2 + self.RECT_HEIGHT,
                self.BAR_FILLED,
                self.BAR - self.PADDING,
                0x00,
            )

            self.epd.text(
                self.percents,
                self.PADDING + self.RECT_WIDTH - 10,
                self.PADDING * 2 + self.RECT_HEIGHT + 10,
                0x00,
            )

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
