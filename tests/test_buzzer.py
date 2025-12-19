from machine import Pin, PWM
from utime import sleep

print("Test buzzer with generator FY248 23mm 3-24V")

try:
    # Initializng
    bzr = PWM(Pin(22))
    print("Setting up frequency...")

    # Setting frequency
    bzr.freq(200)

    # Buzzing
    print("Buzzing!!!")
    bzr.duty_u16(1000)
    sleep(2)

    # Finishing
    print("Did you hear that?!")
    bzr.duty_u16(0)

except Exception as e:
    print(f"Error: {e}")
