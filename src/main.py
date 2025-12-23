from machine import Pin, SPI
import utime
from lib.ds1302 import DS1302
from lib.icnt86 import ICNT86, ICNT_Development
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
        self.SECONDS_IN_DAY = 86400

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

    def calculate_days_left(self):
        """Calculating time to deadline"""

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

        self.days_left = (deadline_timestamp - current_timestamp) // self.SECONDS_IN_DAY

        # Calculating percents
        percent_value = 100 - round((self.days_left / 30) * 100)
        self.percents = f"{percent_value:02d} %"

        # Calculating progress bar width
        self.bar_percentage = 1 - (self.days_left / 30)
        self.BAR_FILLED = round((self.WIDTH - 2 * self.PADDING) * self.bar_percentage)

    def wait_for_touch(self):
        self.tp = ICNT86()
        self.dev = ICNT_Development()
        self.old = ICNT_Development()
        self.tp.ICNT_Init()

        while True:
            self.dev.Touch = 1
            self.tp.ICNT_Scan(self.dev, self.old)
            if self.dev.TouchCount > 0:
                return True
            utime.sleep(0.5)

    def main(self):
        try:
            self.t = self.rtc.date_time()
            self.calculate_days_left()

            self.epd.fill(0xFF)

            # if self.days_left > 0:  # correct condition
            if self.days_left < 0:
                self.draw_countdown()
                self.epd.display(self.epd.buffer)
            # elif self.days_left <= 0:  # correct condition
            elif self.days_left > 0:
                # self.buzzer()
                self.draw_expired()
                self.epd.display(self.epd.buffer)
                if self.wait_for_touch():
                    self.confirmed()

        except Exception as e:
            error = f"Error: {e}"
            print(error)
            self.epd.text(
                error,
                self.PADDING,
                self.HEIGHT // 2,
                0x00,
            )

    def draw_countdown(self):
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

        # Border
        self.epd.rect(
            self.PADDING,
            self.PADDING * 2 + self.RECT_HEIGHT,
            self.WIDTH - 2 * self.PADDING,
            self.BAR - self.PADDING,
            0x00,
        )

        # Progress fill
        self.epd.fill_rect(
            self.PADDING,
            self.PADDING * 2 + self.RECT_HEIGHT,
            self.BAR_FILLED,
            self.BAR - self.PADDING,
            0x00,
        )

        # Text background
        self.epd.fill_rect(
            self.PADDING + self.RECT_WIDTH - 10,
            self.PADDING * 2 + self.RECT_HEIGHT + 8,
            len(self.percents) * 8,
            11,
            0xFF,
        )

        # Percents text
        self.epd.text(
            self.percents,
            self.PADDING + self.RECT_WIDTH - 10,
            self.PADDING * 2 + self.RECT_HEIGHT + 10,
            0x00,
        )

    def draw_expired(self):
        if self.days_left > 0:
            # Frame
            self.epd.rect(
                self.PADDING,
                self.PADDING,
                self.WIDTH - self.PADDING * 2,
                self.HEIGHT - self.PADDING * 2,
                0x00,
            )

            # Text
            self.epd.text(
                "YOU'RE OUT OF TIME!",
                self.PADDING + 70,
                self.HEIGHT // 2 - 35,
                0x00,
            )

            self.epd.text(
                "You are X days late :(",
                self.PADDING + 60,
                self.HEIGHT // 2 - 10,
                0x00,
            )

            self.epd.rect(
                self.WIDTH // 2 - 80,
                self.HEIGHT // 2 + 15,
                160,
                30,
                0x00,
            )

            self.epd.text(
                ">>LENSE CHANGE<<",
                self.WIDTH // 2 - 64,
                self.HEIGHT // 2 + 25,
                0x00,
            )

    def calculate_new_deadline(self, days):
        today = utime.mktime((self.t[0], self.t[1], self.t[2], 0, 0, 0, 0, 0))
        new_timestamp = today + (days * self.SECONDS_IN_DAY)
        new_date = utime.localtime(new_timestamp)
        return f"{new_date[0]}-{new_date[1]:02d}-{new_date[2]:02d}"

    def confirmed(self):
        new_deadline = self.calculate_new_deadline(30)
        save_deadline_data = {"habit": "Changing Lenses", "date": new_deadline}
        with open("next_deadline.json", "w") as f:
            json.dump(save_deadline_data, f)

        self.epd.fill(0xFF)
        # Frame
        self.epd.rect(
            self.PADDING,
            self.PADDING,
            self.WIDTH - self.PADDING * 2,
            self.HEIGHT - self.PADDING * 2,
            0x00,
        )

        # Text
        self.epd.text(
            "CONGRATS!",
            self.PADDING + 70,
            self.HEIGHT // 2 - 35,
            0x00,
        )

        self.epd.text(
            "NEW DEADLINE SET",
            self.PADDING + 60,
            self.HEIGHT // 2 - 10,
            0x00,
        )

        self.epd.text(
            new_deadline,
            self.WIDTH // 2 - 64,
            self.HEIGHT // 2 + 25,
            0x00,
        )
        self.epd.display(self.epd.buffer)

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
