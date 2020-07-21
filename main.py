import os

from lib import RPi_I2C_driver, rotary_encoder

MAIN_MENU = 0
PLAY_MENU = 1
RECORD_MENU = 2

presets = sorted(os.listdir("presets"))





class Menu:

    def __init__(self):
        self.position = 0
        self.menu = MAIN_MENU
        self.rotary = rotary_encoder.RotaryEncoder()
        self.lcd = RPi_I2C_driver.lcd()
        self.set_text()

    def get_preset_name(self):
        if self.position >= len(presets):
            self.position = len(presets) - 1
        elif self.position < 0:
            self.position = 0
        return sorted(os.listdir("presets"))[self.position]

    def set_text(self):
        self.lcd.lcd_clear()
        if self.menu == MAIN_MENU:
            if self.position <= 20:
                self.lcd.lcd_display_string("Play mode  ", 1)
                self.lcd.lcd_display_string("push knob...", 2)
            elif self.position > 20:
                self.lcd.lcd_display_string("Record mode", 1)
                self.lcd.lcd_display_string("push knob...", 2)
        elif self.menu == PLAY_MENU:
            self.lcd.lcd_display_string("Select and push:", 1)
            self.lcd.lcd_display_string(get_preset_name(self.position), 2)

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
            self.set_text()


def main():
    menu = Menu()
    menu.pool()


if __name__ == '__main__':
    main()
