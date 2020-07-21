import glob

from lib import RPi_I2C_driver, rotary_encoder

MAIN_MENU = 0
PLAY_MENU = 1
RECORD_MENU = 2

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("Play mode", 1)
lcd.lcd_display_string("press knob...", 2)


def get_preset_name(position):
    return glob.glob("presets/*")[position]


def set_text(menu, position):
    if menu == MAIN_MENU:
        if position <= 20:
            lcd.lcd_display_string("Play mode  ", 1)
            lcd.lcd_display_string("push knob...", 2)
        elif position > 20:
            lcd.lcd_display_string("Record mode", 1)
            lcd.lcd_display_string("push knob...", 2)
    elif menu == PLAY_MENU:
        lcd.lcd_display_string("Select and push:", 1)
        lcd.lcd_display_string(get_preset_name(position), 2)


class Menu:

    def __init__(self):
        self.position = 0
        self.menu = MAIN_MENU
        self.rotary = rotary_encoder.RotaryEncoder()

    def select(self):
        if self.menu == MAIN_MENU:
            if self.position <= 20:
                self.menu = PLAY_MENU
                self.position = 0

    def pool(self):
        while True:
            message = self.rotary.eventq.get()
            if message == rotary_encoder.RotaryEncoder.LEFT or message == rotary_encoder.RotaryEncoder.RIGHT:
                self.position += message
                print(self.position)
            else:
                self.select()
            set_text(self.menu, self.menu)


def main():
    menu = Menu()
    menu.pool()


if __name__ == '__main__':
    main()
