import time

import serial


class Beamer:

    def __init__(self):
        self.init = True
        try:
            self.ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)
        except:
            self.init = False

    def toggle(self):
        if not self.init:
            return
        packet = bytearray()
        packet.append(0x7E)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x20)
        packet.append(0x31)
        packet.append(0x0D)
        packet.append(0xFF)
        self.ser.write(packet)
        time.sleep(1)

        packet = bytearray()
        packet.append(0x7E)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x30)
        packet.append(0x20)
        packet.append(0x32)
        packet.append(0x0D)
        packet.append(0xFF)
        self.ser.write(packet)

        self.ser.close()
