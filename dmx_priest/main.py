
import os
from datetime import datetime
from os.path import expanduser
from shutil import copyfile
from time import sleep

from dmx_priest import ola, presets_dir, qlc

from dmx_priest.lib import RPi_I2C_driver
from dmx_priest.lib import rotary_encoder
from dmx_priest.lib.beamer import Beamer
from dmx_priest.lib import blackout_button
import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {'beamer_device': '/dev/ttyUSB0',
                     'lcd_address': '0x27'}
MAIN_MENU = 0
PLAY_MENU = 1
RECORD_MENU = 2
QLC_MENU = 3

config_path = expanduser("~") + "/.config/dmx-priest/"
config_file = config_path + "dmx-priest.ini"
user_preset_path = config_path + "presets"


def pool():
    while True:
        sleep(10)


class Menu:
    presets = []
    is_recording = False
    is_playing = False

    def __init__(self, beamer, lcd_address):
        self.position = 0
        self.menu = MAIN_MENU
        self.rotary = rotary_encoder.RotaryEncoder(callback=self.action)
        self.blackout_button = blackout_button.BlackoutButton(callback=self.blackout_button_action)
        self.lcd = RPi_I2C_driver.lcd(address = lcd_address)
        self.set_text()
        self.beamer = beamer

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
                if self.position % 3 == 0:
                    self.lcd.lcd_display_string("Play mode", 1)
                    self.lcd.lcd_display_string("push the knob", 2)
                elif self.position % 3 == 1:
                    if self.beamer.init:
                        self.lcd.lcd_display_string("Beamer", 1)
                    else:
                        self.lcd.lcd_display_string("Beamer error", 1)
                    self.lcd.lcd_display_string("push to toggle", 2)
                else:
                    self.lcd.lcd_display_string("QLC mode", 1)
                    self.lcd.lcd_display_string("push the knob", 2)
            elif self.position <= 30:
                self.lcd.lcd_display_string("Record mode", 1)
                self.lcd.lcd_display_string("push the knob", 2)
            elif self.position > 30:
                self.lcd.lcd_display_string("QLC mode", 1)
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
        elif self.menu == QLC_MENU:
            self.lcd.lcd_display_string("QLC in Progress", 1)
            self.lcd.lcd_display_string("push to stop", 2)


    def select(self):
        self.is_playing = False
        if self.menu == MAIN_MENU:
            if self.position <= 20:
                if self.position % 3 == 0:
                    self.presets = sorted(os.listdir(user_preset_path))
                    self.menu = PLAY_MENU
                    self.position = 0
                    ola.patch_output()
                elif self.position % 3 == 1:
                    self.beamer.toggle()
                else:
                    self.menu = QLC_MENU
                    qlc.start_qlc()
                    print("after start qlc")
            elif self.position <= 30:
                self.menu = RECORD_MENU
                ola.patch_input()
            else:
                self.menu = QLC_MENU
                qlc.start_qlc()
                print("after start qlc")
        elif self.menu == PLAY_MENU:
            self.is_playing = True
            ola.play(user_preset_path + "/" + self.get_preset_name())
            if self.get_preset_name() == "99_blackout.ola":
                self.blackout()
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
        elif self.menu == QLC_MENU:
            self.lcd.lcd_display_string("QLC is stopping..", 1)
            self.lcd.lcd_display_string("please wait...", 2)
            qlc.stop()
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

    def blackout_button_action(self):
        self.blackout()

    def blackout_routine(self, phase):
        ola.patch_output()
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("Power off ("+phase+"/3)", 1)
        self.lcd.lcd_display_string("blackout", 2)
        qlc.stop()
        self.lcd.lcd_display_string("blackout.", 2)
        self.beamer.off()
        sleep(2)
        self.lcd.lcd_display_string("blackout..", 2)
        ola.unpatch()
        sleep(2)
        self.lcd.lcd_display_string("blackout...", 2)
        ola.patch_output()
        sleep(2)
        ola.play(user_preset_path + "/" + "99_blackout.ola")
        self.lcd.lcd_display_string("blackout....", 2)
        sleep(2)
        ola.play(user_preset_path + "/" + "99_blackout.ola")
        sleep(2)
        self.lcd.lcd_display_string("blackout.....", 2)
        ola.stop()
        ola.unpatch()

    def blackout(self):
        self.blackout_routine("1")
        self.blackout_routine("2")
        self.blackout_routine("3")
        self.menu = MAIN_MENU
        self.position = 0
        self.set_text()

def main():
    if not os.path.exists(user_preset_path):
        os.makedirs(user_preset_path)
        copyfile(presets_dir + "/99_blackout.ola", user_preset_path + "/99_blackout.ola")
    if not os.path.exists(config_file):
        with open(config_file, 'w') as conf:
            config.write(conf)
    else:
        config.read(config_file)
    print('Config:')
    print({section: dict(config[section]) for section in config})
    beamer = Beamer(device=config['DEFAULT']['beamer_device'])

    menu = Menu(beamer = beamer, lcd_address = int(config['DEFAULT']['lcd_address'], 0))
    pool()


if __name__ == '__main__':
    main()
