import smbus
import logging
from time import sleep

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class LCD:
    #initializes objects and lcd
    def __init__(self, address=0x20, columns=20, rows=4):
        self.address = address
        self.columns = columns
        self.rows = rows
        self.i2c = smbus.SMBus(1)

        self.cache = {}
        for row in range(rows):
            self.cache[row + 1] = " " * columns
        
        self.backlight = LCD_BACKLIGHT

        self.write(0x03)
        self.write(0x03)
        self.write(0x03)
        self.write(0x02)

        self.write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.write(LCD_CLEARDISPLAY)   
        self.write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)

    def CreateChar(self, location, charmap):
        location &= 0x7 # we only have 8 locations 0-7
        self.write(LCD_SETCGRAMADDR | (location << 3));
        for i in range(8):
            self.write(charmap[i], Rs);

    def SetBacklight(self, backlight):
        self.backlight = LCD_BACKLIGHT if backlight else LCD_NOBACKLIGHT
        self.write(0)

    # clocks EN to latch command
    def strobe(self, data):
        self.i2c.write_byte(self.address, data | En | self.backlight)
        sleep(0.0005)
        self.i2c.write_byte(self.address, ((data & ~En) | self.backlight))
        sleep(0.0001)   

    def writeFourBits(self, data):
        self.i2c.write_byte(self.address, data | self.backlight)
        self.strobe(data)

    # write a command to lcd
    def write(self, cmd, mode=0):
        self.writeFourBits(mode | (cmd & 0xF0))
        self.writeFourBits(mode | ((cmd << 4) & 0xF0))

    # put string function
    def SetText(self, row, text):
        try:
            text = text.ljust(self.columns, " ")[:self.columns]

            if text == self.cache[row]:
                return
            self.cache[row] = text

            if row == 1:
                self.write(0x80)
            if row == 2:
                self.write(0xC0)
            if row == 3:
                self.write(0x94)
            if row == 4:
                self.write(0xD4)

            for char in text:
                self.write(ord(char), Rs)
        except IOError:
            logging.warning("I2C communication error in LCD.SetText")

    # clear lcd and set to home
    def Clear(self):
        try:
            self.write(LCD_CLEARDISPLAY)
            self.write(LCD_RETURNHOME)
        except IOError:
            logging.warning("I2C communication error in LCD.Clear")
