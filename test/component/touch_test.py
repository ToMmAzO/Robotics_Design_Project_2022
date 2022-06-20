# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from digitalio import DigitalInOut, Direction

# set the GPIO input pins

pad1_pin = board.D17
pad2_pin = board.D4

pad1 = DigitalInOut(pad1_pin)
pad2 = DigitalInOut(pad2_pin)

pad1.direction = Direction.INPUT
pad2.direction = Direction.INPUT

pad1_already_pressed = True
pad2_already_pressed = True

while True:

    if pad1.value and not pad1_already_pressed:
        print("Pad 0 pressed")
    pad1_already_pressed = pad1.value

    if pad2.value and not pad2_already_pressed:
        print("Pad 2 pressed")
    pad2_already_pressed = pad2.value

    time.sleep(0.1)
