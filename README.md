# R2D2

## Setup

### Readonly File System

It's a good idea to set the file system on the SD card to readonly to protect it from becoming corrupted if the Raspberry Pi loses power. This is a good guide: https://hallard.me/raspberry-pi-read-only/

### Software and Libraries
```bash
sudo apt-get remove --purge libreoffice* chromium-browser rpi-chromium-mods
sudo apt-get clean
sudo apt-get autoremove
```

Install some software that will be needed:
```bash
sudo pip install adafruit-mcp3008 adafruit-pca9685
sudo apt-get install screen i2c-tools joystick python-pygame python-serial python-bluetooth pi-bluetooth omxplayer
```

### Startup Script

Add the following lines to `/etc/rc.local`:
```bash
# Set the voltage on pin 23 HIGH so the LED can indicate the pi has booted up.
echo 23 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio23/direction
echo 1 > /sys/class/gpio/gpio23/value

# Run the startup script not as sudo.
screen -dm -t "r2d2" bash -c "sudo su pi -c 'python /home/pi/R2D2/startup.py'"
```
