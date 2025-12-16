"""
LCD_1inch28.py - Driver for 1.28 inch Round LCD Display (240x240)

This module provides a driver for the GC9A01 based 1.28 inch round LCD display.
The display uses SPI communication and supports 16-bit RGB565 color format.

Display Specifications:
    - Resolution: 240x240 pixels
    - Interface: SPI
    - Color Format: RGB565 (16-bit)
    - Controller: GC9A01

Usage:
    from lib import LCD_1inch28

    lcd = LCD_1inch28.LCD_1inch28()
    lcd.Init()
    lcd.clear()
    lcd.ShowImage(image)  # PIL Image object
"""

import time
from . import lcdconfig


class LCD_1inch28(lcdconfig.RaspberryPi):
    """
    Driver class for 1.28 inch round LCD display (GC9A01 controller).

    Inherits from lcdconfig.RaspberryPi to access GPIO and SPI functionality.

    Attributes:
        width (int): Display width in pixels (240)
        height (int): Display height in pixels (240)
    """

    width = 240
    height = 240

    def command(self, cmd):
        """
        Send a command byte to the LCD controller.

        Args:
            cmd (int): Command byte to send (0x00-0xFF)
        """
        self.digital_write(self.DC_PIN, self.GPIO.LOW)
        self.spi_writebyte([cmd])
        
    def data(self, val):
        """
        Send a data byte to the LCD controller.

        Args:
            val (int): Data byte to send (0x00-0xFF)
        """
        self.digital_write(self.DC_PIN, self.GPIO.HIGH)
        self.spi_writebyte([val])
        
    def reset(self):
        """
        Perform a hardware reset of the display.

        Toggles the reset pin HIGH -> LOW -> HIGH with 10ms delays
        to reset the LCD controller to its initial state.
        """
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        
    def Init(self):
        """
        Initialize the LCD display.

        Performs module initialization, hardware reset, and sends the
        complete initialization sequence for the GC9A01 controller.
        This configures power settings, gamma correction, display timing,
        and enables the display.

        Must be called before any other display operations.
        """
        self.module_init()   
        self.reset()
        
        self.command(0xEF)
        self.command(0xEB)
        self.data(0x14)
        
        self.command(0xFE)			 
        self.command(0xEF) 

        self.command(0xEB)	
        self.data(0x14)

        self.command(0x84)			
        self.data(0x40) 

        self.command(0x85)			
        self.data(0xFF)

        self.command(0x86)			
        self.data(0xFF) 

        self.command(0x87)		
        self.data(0xFF)

        self.command(0x88)			
        self.data(0x0A)

        self.command(0x89)			
        self.data(0x21)

        self.command(0x8A)		
        self.data(0x00)

        self.command(0x8B)			
        self.data(0x80) 

        self.command(0x8C)			
        self.data(0x01) 

        self.command(0x8D)			
        self.data(0x01) 

        self.command(0x8E)			
        self.data(0xFF) 

        self.command(0x8F)			
        self.data(0xFF) 


        self.command(0xB6)
        self.data(0x00)
        self.data(0x20)

        self.command(0x36)
        self.data(0x08)
    
        self.command(0x3A)			
        self.data(0x05) 


        self.command(0x90)			
        self.data(0x08)
        self.data(0x08)
        self.data(0x08)
        self.data(0x08) 

        self.command(0xBD)			
        self.data(0x06)
	
        self.command(0xBC)			
        self.data(0x00)	

        self.command(0xFF)			
        self.data(0x60)
        self.data(0x01)
        self.data(0x04)

        self.command(0xC3)			
        self.data(0x13)
        self.command(0xC4)			
        self.data(0x13)

        self.command(0xC9)		
        self.data(0x22)

        self.command(0xBE)			
        self.data(0x11)

        self.command(0xE1)		
        self.data(0x10)
        self.data(0x0E)

        self.command(0xDF)			
        self.data(0x21)
        self.data(0x0c)
        self.data(0x02)

        self.command(0xF0)   
        self.data(0x45)
        self.data(0x09)
        self.data(0x08)
        self.data(0x08)
        self.data(0x26)
        self.data(0x2A)

        self.command(0xF1)    
        self.data(0x43)
        self.data(0x70)
        self.data(0x72)
        self.data(0x36)
        self.data(0x37)  
        self.data(0x6F)


        self.command(0xF2)   
        self.data(0x45)
        self.data(0x09)
        self.data(0x08)
        self.data(0x08)
        self.data(0x26)
        self.data(0x2A)

        self.command(0xF3)  
        self.data(0x43)
        self.data(0x70)
        self.data(0x72)
        self.data(0x36)
        self.data(0x37) 
        self.data(0x6F)

        self.command(0xED)	
        self.data(0x1B) 
        self.data(0x0B) 

        self.command(0xAE)			
        self.data(0x77)
	
        self.command(0xCD)			
        self.data(0x63)		


        self.command(0x70)			
        self.data(0x07)
        self.data(0x07)
        self.data(0x04)
        self.data(0x0E) 
        self.data(0x0F)
        self.data(0x09)
        self.data(0x07)
        self.data(0x08)
        self.data(0x03)

        self.command(0xE8)			
        self.data(0x34)

        self.command(0x62)			
        self.data(0x18)
        self.data(0x0D)
        self.data(0x71)
        self.data(0xED)
        self.data(0x70)
        self.data(0x70)
        self.data(0x18)
        self.data(0x0F)
        self.data(0x71)
        self.data(0xEF)
        self.data(0x70) 
        self.data(0x70)

        self.command(0x63)			
        self.data(0x18)
        self.data(0x11)
        self.data(0x71)
        self.data(0xF1)
        self.data(0x70) 
        self.data(0x70)
        self.data(0x18)
        self.data(0x13)
        self.data(0x71)
        self.data(0xF3)
        self.data(0x70) 
        self.data(0x70)

        self.command(0x64)			
        self.data(0x28)
        self.data(0x29)
        self.data(0xF1)
        self.data(0x01)
        self.data(0xF1)
        self.data(0x00)
        self.data(0x07)

        self.command(0x66)			
        self.data(0x3C)
        self.data(0x00)
        self.data(0xCD)
        self.data(0x67)
        self.data(0x45)
        self.data(0x45)
        self.data(0x10)
        self.data(0x00)
        self.data(0x00)
        self.data(0x00)

        self.command(0x67)			
        self.data(0x00)
        self.data(0x3C)
        self.data(0x00)
        self.data(0x00)
        self.data(0x00)
        self.data(0x01)
        self.data(0x54)
        self.data(0x10)
        self.data(0x32)
        self.data(0x98)

        self.command(0x74)			
        self.data(0x10)	
        self.data(0x85)	
        self.data(0x80)
        self.data(0x00) 
        self.data(0x00)
        self.data(0x4E)
        self.data(0x00)					
        
        self.command(0x98)		
        self.data(0x3e)
        self.data(0x07)

        self.command(0x35)	
        self.command(0x21)

        self.command(0x11)
        time.sleep(0.12)
        self.command(0x29)
        time.sleep(0.02)
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        """
        Set the drawing window area on the display.

        Defines the rectangular region where subsequent pixel data
        will be written. Uses CASET (0x2A) and RASET (0x2B) commands.

        Args:
            Xstart (int): Starting X coordinate (0-239)
            Ystart (int): Starting Y coordinate (0-239)
            Xend (int): Ending X coordinate (1-240, exclusive)
            Yend (int): Ending Y coordinate (1-240, exclusive)
        """
        # Set the X coordinates
        self.command(0x2A)
        self.data(0x00)               #Set the horizontal starting point to the high octet
        self.data(Xstart)      #Set the horizontal starting point to the low octet
        self.data(0x00)               #Set the horizontal end to the high octet
        self.data(Xend - 1) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data(Ystart)
        self.data(0x00)
        self.data(Yend - 1)

        self.command(0x2C) 
        
    def ShowImage(self, Image):
        """
        Display a PIL Image on the LCD.

        Converts the image from RGB888 to RGB565 format and writes
        the pixel data to the display via SPI in 4096-byte chunks.

        Args:
            Image (PIL.Image): A PIL Image object. Must be exactly
                240x240 pixels in RGB mode.

        Raises:
            ValueError: If the image dimensions don't match the display
                (240x240 pixels).

        Note:
            RGB565 conversion:
            - Red: 5 bits (bits 15-11)
            - Green: 6 bits (bits 10-5)
            - Blue: 5 bits (bits 4-0)
        """
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])		
    
    def clear(self):
        """
        Clear the display to white.

        Fills the entire display with white pixels (0xFF) by writing
        a buffer of white pixel data to the full display area.
        Data is sent in 4096-byte chunks via SPI.
        """
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	        
        

