# R2D2

## Setup

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
