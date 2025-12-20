### Mnematic

A simple device that keeps you reminded about your habits.

#### Hardware components

- Raspberry Pi Pico H - RP2040 ARM Cortex M0+
- E-paper - 2,9'' 296x128px - SPI/I2C - B&W - Waveshare 20051
- Buzzer w/ Generator FY248 23mm 3-24V
- Real Time Clock - DS1302 RTC

### Pinout

```
                         ┌─────────────────┐
                         │    ╔══USB══╗    │
                  GP0  ──┤ 01 ║       ║ 40 ├── VBUS
                  GP1  ──┤ 02 ║       ║ 39 ├── VSYS ------- eInk (Input Voltage)
                  GND  ──┤ 03 ║       ║ 38 ├── GND       
  eInk (KEY0)---  GP2  ──┤ 04 ║       ║ 37 ├── 3V3_EN
  eInk (KEY1)---  GP3  ──┤ 05 ║       ║ 36 ├── 3V3(OUT) --- eInk (Input Voltage)
                  GP4  ──┤ 06 ║       ║ 35 ├── ADC_VREF
                  GP5  ──┤ 07 ║       ║ 34 ├── GP28 
                  GND  ──┤ 08 ║       ║ 33 ├── GND
  eInk ---------  GP6  ──┤ 09 ║       ║ 32 ├── GP27 
  eInk ---------  GP7  ──┤ 10 ║       ║ 31 ├── GP26 
  eInk ---------  GP8  ──┤ 11 ║       ║ 30 ├── RUN -------- eInk (Reset Button)
  eInk ---------  GP9  ──┤ 12 ║       ║ 29 ├── GP22 ------- Buzzer (SIG)  
                  GND  ──┤ 13 ║       ║ 28 ├── GND -------- Buzzer (GND)
  eInk ---------  GP10 ──┤ 14 ║       ║ 27 ├── GP21     
  eInk ---------  GP11 ──┤ 15 ║       ║ 26 ├── GP20 ------- RTC (RST)
  eInk ---------  GP12 ──┤ 16 ║       ║ 25 ├── GP19 ------- RTC (DAT)
  eInk ---------  GP13 ──┤ 17 ║       ║ 24 ├── GP18 ------- RTC (CLK)
  eInk (GND)----  GND  ──┤ 18 ║       ║ 23 ├── GND -------- RTC (GND)
                  GP14 ──┤ 19 ║       ║ 22 ├── GP17 ------- eInk
  eInk ---------  GP15 ──┤ 20 ║       ║ 21 ├── GP16 ------- eInk
                         │    ╚═══════╝    │
                         └─────────────────┘
                              
```

```
