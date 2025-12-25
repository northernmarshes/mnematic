# Run only when the time is not set !!!
# RTC keeps track of time with the battery
# Run with "python3 sync_time.py" not with mpremote

import subprocess
from datetime import datetime

now = datetime.now()
cmd = f"""
from machine import Pin
from lib.ds1302 import DS1302
rtc = DS1302(Pin(18), Pin(19), Pin(20))
rtc.start()
rtc.date_time([{now.year}, {now.month}, {now.day}, {now.isoweekday()}, {now.hour}, {now.minute}, {now.second}])
print("Synchronized!")
"""

subprocess.run(["mpremote", "exec", cmd])
