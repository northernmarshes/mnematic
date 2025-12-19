from machine import Pin, SPI
import time

print("Test Waveshare 2.9 Portrait")

try:
    from Pico_ePaper_2_9 import EPD_2in9_Portrait

    print("Initialisation...")
    epd = EPD_2in9_Portrait()

    print("Clearing (white)...")
    epd.Clear(0xFF)

    time.sleep(1)

    print("Drawing...")
    epd.fill(0xFF)
    epd.text("MNEMATIC", 10, 50, 0x00)
    epd.text("TIME LEFT", 10, 70, 0x00)
    epd.rect(10, 120, 100, 30, 0x00)
    epd.text("Days: 0/30", 15, 128, 0x00)

    epd.display(epd.buffer)

    print("Test passed!")

    time.sleep(2)
    epd.sleep()

except Exception as e:
    print(f"Error: {e}")
