from lib import RPi_I2C_driver, rotary_encoder

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("Play mode", 1)
lcd.lcd_display_string("press knob...", 2)
rotary = rotary_encoder.RotaryEncoder()
position = 0

while True:
    message = rotary.eventq.get()
    if message == rotary.LEFT or message == rotary.RIGHT:
        position += message
        print(position)
    else:
        print("button")
