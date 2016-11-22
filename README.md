# R2D2

## Setup

### Readonly File System

It's a good idea to set the file system on the SD card to readonly to protect it from becoming corrupted if the Raspberry Pi loses power. This is a good guide: https://hallard.me/raspberry-pi-read-only/

### Startup Script

Add the following lines to `/etc/rc.local`:
```bash
# Set the voltage on pin 23 HIGH so the LED can indicate the pi has booted up.
echo 23 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio23/direction
echo 1 > /sys/class/gpio/gpio23/value

# Run the startup script.
screen -dm -t "r2d2" bash -c "python /home/pi/R2D2/startup.py"
```
