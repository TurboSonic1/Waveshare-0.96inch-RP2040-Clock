# Waveshare-0.96inch-RP2040-Clock
Just a simple clock that you can set manually that's pretty accurate without relying on ntp, other libraries, or an RTC.

The date is in M/D/Y format for 0.96 inch screens and displays in 24 hour time

±1ms precision every second.

Note: This is written in MICROPYTHON NOT PYTHON, you cannot use this in python code directly without modifying the code slightly but it shouldn't be more than a few lines you need to change on the actual logic of it.