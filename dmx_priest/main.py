import os
from datetime import datetime
from os.path import expanduser
from shutil import copyfile
from time import sleep

from dmx_priest import ola, presets_dir

from dmx_priest.lib import RPi_I2C_driver
from dmx_priest.lib import rotary_encoder
from dmx_priest.lib.beamer import Beamer

MAIN_MENU = 0
PLAY_MENU = 1
RECORD_MENU = 2

user_preset_path = expanduser("~") + "/.config/dmx-priest/presets"
beamer = Beamer


def pool():
    while True:
        sleep(10)


class Menu:
    presets = []
    is_recording = False
    is_playing = False

    def __init__(self):
        self.position = 0
        self.menu = MAIN_MENU
        self.rotary = rotary_encoder.RotaryEncoder(callback=self.action)
        self.lcd = RPi_I2C_driver.lcd()
        self.set_text()

    def get_preset_name(self):
        if self.position >= len(self.presets):
            self.position = len(self.presets) - 1
        elif self.position < 0:
            self.position = 0
        return sorted(self.presets)[self.position]

    def set_text(self):
        self.lcd.lcd_clear()
        if self.menu == MAIN_MENU:
            if self.position <= 20:
                if self.position % 2 == 0:
                    self.lcd.lcd_display_string("Play mode", 1)
                    self.lcd.lcd_display_string("push the knob", 2)
                else:
                    self.lcd.lcd_display_string("Beamer", 1)
                    self.lcd.lcd_display_string("push to toggle", 2)
            elif self.position > 20:
                self.lcd.lcd_display_string("Record mode", 1)
                self.lcd.lcd_display_string("push the knob", 2)
        elif self.menu == PLAY_MENU:
            if self.is_playing:
                self.lcd.lcd_display_string("Playing:", 1)
            else:
                self.lcd.lcd_display_string("Turn and push:", 1)
            self.lcd.lcd_display_string(self.get_preset_name(), 2)
        elif self.menu == RECORD_MENU:
            if self.is_recording:
                self.lcd.lcd_display_string("Rec in progress", 1)
                self.lcd.lcd_display_string("push to stop", 2)
            else:
                self.lcd.lcd_display_string("Ready to record", 1)
                self.lcd.lcd_display_string("push to start", 2)

    def select(self):
        self.is_playing = False
        if self.menu == MAIN_MENU:
            if self.position <= 20:
                if self.position % 2 == 0:
                    self.presets = sorted(os.listdir(user_preset_path))
                    self.menu = PLAY_MENU
                    self.position = 0
                    ola.patch_output()
                else:
                    beamer.toggle()
            else:
                self.menu = RECORD_MENU
                ola.patch_input()
        elif self.menu == PLAY_MENU:
            self.is_playing = True
            ola.play(user_preset_path + "/" + self.get_preset_name())
            if self.get_preset_name() == "99_blackout.ola":
                sleep(1)
                ola.stop()
                ola.unpatch()
                self.menu = MAIN_MENU
                self.position = 0
        elif self.menu == RECORD_MENU:
            self.is_recording = not self.is_recording
            if self.is_recording:
                now = datetime.now()
                name = now.strftime("%Y.%m.%d %H:%M")
                ola.record(user_preset_path + "/" + name + ".ola")
            else:
                ola.stop()
                self.menu = MAIN_MENU
                self.position = 0

    def action(self, message):
        if message == rotary_encoder.RotaryEncoder.LEFT or message == rotary_encoder.RotaryEncoder.RIGHT:
            self.position += message
        else:
            self.select()
        if self.position < 0:
            self.position = 0
        self.set_text()


def main():
    if not os.path.exists(user_preset_path):
        os.makedirs(user_preset_path)
        copyfile(presets_dir + "/99_blackout.ola", user_preset_path + "/99_blackout.ola")
    Menu()
    pool()


if __name__ == '__main__':
    main()
