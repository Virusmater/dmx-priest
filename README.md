# dmx-priest
dmx-priest is a cheap DIY alternative to an expensive commercial DMX Recall Units.
## How to use
1. Spin the knob to the right (more than 20 time in order to avoid misclicks) until screen wound't say "Record mode - push the knob".
2. Push the knob. Screen: "Ready to record - push to start"
3. Prepare your light table or any other source of Art-Net signal
4. Push the knob to start recording. Screen: "Rec in progress - push to stop"
5. Start desired light scene on the source. dmx-priest will record it
6. Push the knob to stop the recording. Screen: "Play mode - push the knob"
7. Push the knob to enter the Play mode. You will see your recoding in the format YYYY.mm.dd HH:MM
8. Select your recording to playback or select 99_blackout to exit and stop the program
## Situation
We have a lights console (Avolites Titan Quartz) for big shows and a manual control. 
Console connects goes to Art-Net to DMX converter with two DMX output ports (dmXLAN Buddy).  

We need a device that would be easy to operate for everybody. It should record and playback scenes from the console without pluggin the console itself.
## Device in case
![device](/device.jpg?raw=true "Device in case")
## Hardware
- raspberry pi
- lcd display (<https://opencircuit.shop/Product/LCD-display-1602-symbols-2-rows-16-columns-.>)
- rotary encoder (<https://opencircuit.shop/Product/Rotary-Encoder-Module>)
- jump wires
- optional: switch

### Connect LCD
- GND to Pin 6 (Ground)
- VCC to Pin 4 (5V power)
- SDA to Pin 3 (GPIO 2)
- SLC to Pin 5 (GPIO 3)

### Connect Rotary Encoder
- CLK to Pin 12 (GPIO 18)
- DT to Pin 13 (GPIO 27)
- SW to Pin 11 (GPIO 17)
- \+ to Pin 1 (3V3 power)
- GND to Pin 14 (Ground)

### Optionally - on/off switch
I just broke Micro USB cable in between and soldered a button in case Raspberry with hang

## Software
### OS
install Raspberry Pi OS (32-bit) Lite using Etcher  

add file "ssh" to /boot in order to enable SSH access  
```bash
youruser@homepc:~ $ ssh pi@[Pi-IP-address]
```
Upgrade your OS:
```bash
pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get dist-upgrade
```
### Open Lightning Architecture
Install software to build Open Lightning Architecture and also few python libraries
```bash
pi@raspberrypi:~ $ sudo apt-get install git autoconf libtool bison flex uuid-dev libcppunit-dev python-protobuf python-numpy protobuf-compiler  libmicrohttpd-dev libprotoc-dev i2c-tools python3-smbus python3-gpiozero python3-pip3
pi@raspberrypi:~ $ git clone https://github.com/OpenLightingProject/ola.git
pi@raspberrypi:~ $ cd ola
```
compile and install ola. it will take some (a lot) time:
```bash
pi@raspberrypi:~/ola $ autoreconf -i
pi@raspberrypi:~/ola $ ./configure --enable-rdm-tests
pi@raspberrypi:~/ola $ make
pi@raspberrypi:~/ola $ sudo make install
```
load libraries and start daemon:
```bash
pi@raspberrypi:~/ola $ sudo ldconfig
pi@raspberrypi:~/ola $ olad -l 3
```
check if it works
http://[Pi-IP-address]:9090/ola.html  

create a systemd service for autoload of olad:  

create .service file
```
pi@raspberrypi:~ $ sudo nano /etc/systemd/system/olad.service
```
and add inside:
```
[Unit]
Description=OLA daemon
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=olad

[Install]
WantedBy=multi-user.target
```
start service and enable autostart:
```bash
pi@raspberrypi:~ $ sudo systemctl start olad
pi@raspberrypi:~ $ sudo systemctl enable olad
```
### I2C interface
enable i2c interface:
```
pi@raspberrypi:~ $ sudo raspi-config
```
Inside of raspi-config go to "Interfacing Options" > "I2C" > "enable"
then reboot your RPi
```bash
pi@raspberrypi:~ $ sudo reboot
```
get address of the LCD display:
```bash
pi@raspberrypi:~/dmx-priest $ sudo i2cdetect -y 1
```
In my case it was 3f. Change it in RPi_I2C_driver.py if needed (better to take it from the variable, but it isn't done yet)
### Static IP (optional)
Just to be sure let's set on Raspberry Pi static IP in 2.x.x.x range.  
Add to the end of /etc/dhcpcd.conf following lines:
```bash
# Example static IP configuration:
interface eth0
static ip_address=2.150.43.69/24
static routers=2.124.1.1
static domain_name_servers=2.124.1.1
```

### dmx-priest
install application for recording and playing presets:
```bash
pi@raspberrypi:~ $ sudo pip3 install git+https://github.com/Virusmater/dmx-priest
```
doing the same what did for olad:
```bash
pi@raspberrypi:~ $ nano /etc/systemd/system/dmx-priest.service 
[Unit]
Description=dmx-priest
Requires=olad.service
After=network.target olad.service
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=dmx-priest

[Install]
WantedBy=multi-user.target

pi@raspberrypi:~ $ sudo systemctl start dmx-priest
pi@raspberrypi:~ $ sudo systemctl enable dmx-priest
```