from lib import RPi_I2C_driver, rotary_encoder

MAIN_MENU = 0
PLAY_MENU = 1
RECORD_MENU = 2

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("Play mode", 1)
lcd.lcd_display_string("press knob...", 2)
rotary = rotary_encoder.RotaryEncoder()
position = 0
menu = MAIN_MENU


def set_text(menu, position):
    if menu == MAIN_MENU:
        if position <= 20:
            lcd.lcd_display_string("Play mode", 1)
            lcd.lcd_display_string("press knob...", 2)
        elif position > 20:
            lcd.lcd_display_string("Record mode", 1)
            lcd.lcd_display_string("press knob...", 2)


while True:
    message = rotary.eventq.get()
    if message == rotary.LEFT or message == rotary.RIGHT:
        position += message
        print(position)
    else:
        print("button")
    set_text(menu, position)
