from lib import RPi_I2C_driver, rotary_encoder

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("Play mode", 1)
lcd.lcd_display_string("press knob...", 2)

while True:
    rotary = rotary_encoder()
    message = rotary.eventq.get()
    print(message)
