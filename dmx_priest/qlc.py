import subprocess
import os
from time import sleep


def unpatch():
    # output ports
    subprocess.run(["ola_patch", "-d", "2", "-r", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-d", "2", "-r", "-p", "1", "-u", "1"])
    # input ports
    subprocess.run(["ola_patch", "-i", "-d", "2", "-r", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-i", "-d", "2", "-r", "-p", "1", "-u", "1"])


def start_qlc():
    unpatch()
    os.environ["QT_QPA_PLATFORM"] = 'offscreen'
    subprocess.Popen(["qlcplus", "-m", "-n", "-w", "-p", "-d", "0", "-o", "/home/pi/acu-lite.qxw"])

def stop():
    my_pid = os.popen('ps --no-headers -C qlcplus').read(5)
    if my_pid != "":
        my_pid = int(my_pid)
        subprocess.run(["killall", "qlcplus"])
        sleep(30)
