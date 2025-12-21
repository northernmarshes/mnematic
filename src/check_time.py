# Program checks current time on RTC module
# Run with: mpremote run check_time.py
from machine import Pin, SPI
from lib.ds1302 import DS1302

rtc = DS1302(Pin(18), Pin(19), Pin(20))
time = rtc.date_time()

print(
    "Current time:",
    "\n",
    "Year:",
    time[0],
    "\n",
    "Month:",
    time[1],
    "\n",
    "Day:",
    time[2],
    "\n",
    "Weekday:",
    time[3],
    "\n",
    "Hour:",
    time[4],
    "\n",
    "Minute:",
    time[5],
    "\n",
    "Second:",
    time[6],
)
