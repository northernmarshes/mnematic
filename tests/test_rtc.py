from machine import Pin
import framebuf

print("Test DS1302 RTC (real time clock)")

try:
    from lib.ds1302 import DS1302
    from Pico_ePaper_2_9 import EPD_2in9_Portrait

    # RTC
    rtc = DS1302(Pin(18), Pin(19), Pin(20))
    rtc.start()

    # Setting time manually - better avoid
    # rtc.date_time([2025, 12, 19, 5, 20, 56, 0])

    epd = EPD_2in9_Portrait()

    WIDTH = 128
    HEIGHT = 296

    # Bufor
    buf = bytearray(WIDTH * HEIGHT // 8)
    fb = framebuf.FrameBuffer(buf, WIDTH, HEIGHT, framebuf.MONO_HLSB)

    # Prepering screen
    fb.fill(0xFF)

    # Read time
    t = rtc.date_time()

    # Text
    fb.text(f"{t[4]:02d}:{t[5]:02d}:{t[6]:02d}", 10, 50, 0x00)
    fb.text(f"{t[2]:02d}.{t[1]:02d}.{t[0]}", 10, 70, 0x00)

    # Send
    epd.display(buf)
    epd.sleep()

    print("Can you see the time?!")

except Exception as e:
    print(f"Error: {e}")
