import time

import serial


class Beamer:

    def __init__(self, device):
        self.init = False
        self.device = device
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(
                port=self.device,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)
        except Exception as e:
            self.init = False
            print("Error during serial port init:", e)
        else:
            self.init = True

    def toggle(self):
        if not self.init:
            self.connect()
            return
        try:
            if(self.ser.isOpen() == False):
                self.ser.open()
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
        except Exception as e:
            self.init = False
            print("Error during beamer toggle:", e)
        finally:
            self.ser.close()

    def off(self):
        if not self.init:
            self.connect()
            return
        try:
            if(self.ser.isOpen() == False):
                self.ser.open()
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
        except Exception as e:
            self.init = False
            print("Error during beamer off:", e)
        finally:
            self.ser.close()

