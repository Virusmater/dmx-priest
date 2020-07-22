import subprocess


def unpatch():
    # output ports
    subprocess.run(["ola_patch", "-d", "2", "-r", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-d", "2", "-r", "-p", "1", "-u", "1"])
    # input ports
    subprocess.run(["ola_patch", "-i", "-d", "2", "-r", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-i", "-d", "2", "-r", "-p", "1", "-u", "1"])


def patch_input():
    unpatch()
    subprocess.run(["ola_patch", "-d", "2", "-i", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-d", "2", "-i", "-p", "1", "-u", "1"])


def patch_output():
    unpatch()
    subprocess.run(["ola_patch", "-d", "2", "-p", "0", "-u", "0"])
    subprocess.run(["ola_patch", "-d", "2", "-p", "1", "-u", "1"])


def stop():
    subprocess.run(["killall", "ola_recorder"])


def play(preset):
    stop()
    preset = "presets/" + preset
    subprocess.Popen(["ola_recorder", "--playback", preset, "-i", "0"])


def record(preset):
    stop()
    preset = "presets/" + preset
    subprocess.Popen(["ola_recorder", "-u", "0,1", "-r", preset])
