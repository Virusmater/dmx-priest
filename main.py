from lib import RPi_I2C_driver

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("Hello World!", 1)