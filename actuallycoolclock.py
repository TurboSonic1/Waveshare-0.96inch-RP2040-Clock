from machine import Pin,SPI,PWM
import framebuf
import time
import math

#color is BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000
# Somehow helps intialize lcd I think
class LCD_0inch96(framebuf.FrameBuffer):
    def __init__(self):
    
        self.width = 160
        self.height = 80
        
        self.cs = Pin(9,Pin.OUT)
        self.rst = Pin(12,Pin.OUT)
#        self.bl = Pin(13,Pin.OUT)
        self.cs(1)
        # pwm = PWM(Pin(13))#BL
        # pwm.freq(1000)        
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(10),mosi=Pin(11),miso=None)
        self.dc = Pin(8,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.Init()
        self.SetWindows(0, 0, self.width-1, self.height-1)
        
    def reset(self):
        self.rst(1)
        time.sleep(0.2) 
        self.rst(0)
        time.sleep(0.2)         
        self.rst(1)
        time.sleep(0.2) 
        
    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def backlight(self,value):#value:  min:0  max:1000
        pwm = PWM(Pin(13))#BL
        pwm.freq(1000)
        if value>=1000:
            value=1000
        data=int (value*65536/1000)       
        pwm.duty_u16(data)  
        
    def Init(self):
        self.reset() 
        self.backlight(10000)  
        
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x21) 
        self.write_cmd(0x21) 

        self.write_cmd(0xB1) 
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB2)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB3) 
        self.write_data(0x05)  
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB4)
        self.write_data(0x03)

        self.write_cmd(0xC0)
        self.write_data(0x62)
        self.write_data(0x02)
        self.write_data(0x04)

        self.write_cmd(0xC1)
        self.write_data(0xC0)

        self.write_cmd(0xC2)
        self.write_data(0x0D)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8D)
        self.write_data(0x6A)   

        self.write_cmd(0xC4)
        self.write_data(0x8D) 
        self.write_data(0xEE) 

        self.write_cmd(0xC5)
        self.write_data(0x0E)    

        self.write_cmd(0xE0)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x02)
        self.write_data(0x03)
        self.write_data(0x0E)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x12)
        self.write_data(0x27)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x03)
        self.write_data(0x03)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x02)
        self.write_data(0x08)
        self.write_data(0x0A)
        self.write_data(0x13)
        self.write_data(0x26)
        self.write_data(0x36)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0x36)
        self.write_data(0xA8)

        self.write_cmd(0x29) 
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend):#example max:0,0,159,79
        Xstart=Xstart+1
        Xend=Xend+1
        Ystart=Ystart+26
        Yend=Yend+26
        self.write_cmd(0x2A)
        self.write_data(0x00)              
        self.write_data(Xstart)      
        self.write_data(0x00)              
        self.write_data(Xend) 

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)

        self.write_cmd(0x2C) 
        
    def display(self):
    
        self.SetWindows(0,0,self.width-1,self.height-1)       
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
# Everything above this line I have no idea how it works            
    
if __name__=='__main__':
    # Setting up variables here
    ignorelol = 5
    exceedsmax60 = 60
    nowzero = 0
    add1 = 1
    exceedsmax24 = 24
    exceedsmax32 = 32
    exceedsmax31 = 31
    exceedsmax12 = 12
    leapyear = 29
    notleapyear = 28
    nowone = 1
    isitleapyear = 29
    omgnewyear = 13

    # Actual code
    lcd = LCD_0inch96()   
    lcd.fill(BLACK)   
    lcd.text("Check terminal",5,15,GREEN)
    lcd.display()
    year = input("Please set year") # You have to set time manually
    month = input("Please set month")
    day = input("Please set day")
    hours = input("Please set hour")
    minutes = input("Please set minute")
    seconds = input("Please set seconds")
    while ignorelol == 5:
        start = time.ticks_us()
        #Converting strings to ints for modifying
        combined_seconds = int(add1) + int(seconds) 
        combined_minutes = int(minutes)
        combined_hours = int(hours)
        combined_day = int(day)
        combined_month = int(month)
        combined_year = int(year)
        # Code below does the actual logic for time
        if combined_seconds == int(exceedsmax60): 
            combined_seconds = int(nowzero)
            combined_minutes = int(add1) + int(minutes)
            if combined_minutes == int(exceedsmax60): # It looks horribly optimized but actually is ok since it only runs when it gets to the next minute/hour etc
                combined_minutes = int(nowzero)
                combined_hours = int(add1) + int(hours)
                if combined_hours == int(exceedsmax24):
                    combined_hours = int(nowzero)
                    combined_day = int(add1) + int(day)
                    if (combined_month %2 == 0):
                        if combined_day == int(exceedsmax31):
                            combined_day = int(nowone)
                            combined_month = int(addone)
                            if combined_month == int(omgnewyear):
                                combined_year = int(addone)
                                combined_month = int(nowone)
                           
                    elif (combined_month == 2):
                        if (combined_year %4 == 0): # have to account for leap year 
                            if combined_day == int(leapyear):
                                    combined_day = int(nowone)
                                    combined_month = int(addone)
                        else:
                            if combined_day == int(notleapyear):
                                combined_day = int(nowone)
                                combined_month = int(addone)
                    else:
                        if combined_day == int(exceedsmax32):
                            combined_day = int(nowone)
                            combined_month = int(addone)
                            if combined_month == int(omgnewyear):
                                combined_year = int(addone)
                                combined_month = int(nowone)
        # Converting everything back to string to display on screen
        seconds = str(combined_seconds) 
        minutes = str(combined_minutes)
        hours = str(combined_hours)
        day = str(combined_day)
        month = str(combined_month)
        year = str(combined_year)
        lcd.fill(BLACK)
        lcd.text( (month) + "/" + (day) + "/" + (year),0,0,GREEN)
        lcd.text( (hours) + ":" + (minutes) + ":" + (seconds),0,15,GREEN)
        lcd.display()
        end = time.ticks_us()
        diff = time.ticks_diff(end, start)
        precisemicroseconds = 1000000 - diff
        time.sleep_us(precisemicroseconds)
