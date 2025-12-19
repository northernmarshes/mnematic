from machine import Pin, SPI

print("Test Waveshare 2.9 Landscape Class")

try:
    from Pico_ePaper_2_9 import EPD_2in9_Landscape

    # Creating an object
    print("Initialisation...")
    epd = EPD_2in9_Landscape()

    # Clearing
    print("Clearing...")
    epd.Clear(0xFF)

    # Drawing text
    print("Drawing...")
    epd.fill(0xFF)
    epd.text("MNEMATIC", 10, 10, 0x00)
    epd.text("TIME LEFT", 10, 20, 0x00)
    epd.rect(10, 50, 100, 30, 0x00)
    epd.text("Days: 0/30", 15, 60, 0x00)
    epd.display(epd.buffer)

    # Finishing
    print("Can you see the text?!")
    epd.sleep()

except Exception as e:
    print(f"Error: {e}")
