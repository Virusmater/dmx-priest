import subprocess
import os
from time import sleep
from ola import unpatch

def start_qlc():
    unpatch()
    os.environ["QT_QPA_PLATFORM"] = 'offscreen'
    subprocess.Popen(["qlcplus", "-m", "-n", "-w", "-p", "-o", "/home/pi/acu-lite.qxw"])

def stop():
    my_pid = os.popen('ps --no-headers -C qlcplus').read(5)
    if my_pid != "":
        my_pid = int(my_pid)
        subprocess.run(["killall", "qlcplus"])
        sleep(30)
