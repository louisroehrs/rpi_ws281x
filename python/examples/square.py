#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import math
import random
import os
import os.path
import string

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels.
LED_WIDTH      = 16      # width.
LED_HEIGHT     = 16      # height.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

brightness = .10


# Define functions which animate LEDs in various ways.

def candles(strip, iterations=1, wait_ms=20000):
    """Wipe color across display a pixel at a time."""
    for j in range(256*iterations):
        time.sleep(wait_ms/1000.0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(int(math.sin(i*j)*random.randint(0, 128)+128),int(math.sin(i*j)*random.uniform(0,90)+128), 0))
        strip.show()
        if shouldstop():
            return

def setbrightness(b=1.0):
    """set the brightness 0 - 1"""
    brightness = b

def copcar(strip, iterations=1, width=4, wait_ms=1000):
    """Wipe color across display a pixel at a time."""
    for j in range(256*iterations):
        time.sleep(wait_ms/1000.0)
        section = width*3;
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,
                                Color(0,
                                      int(255*((i+j*4) % section < width)),
                                      int(255*((i+j*4) % section >= 2*width))
                                ))
        strip.show()
        if shouldstop():
            return


def runway(strip, iterations=1, width=6, wait_ms=2000):
    """Wipe color across display a pixel at a time."""
    j=0
    while (j < iterations or iterations == -1):
        res = 20;   #resolution, more steps equals smoother animation.
        for x in range(20):
            time.sleep(wait_ms/20000.0)
            section = width*2;
            for i in range(strip.numPixels()):
                strip.setPixelColor(i,         #bright cycle                                off cycle
                                    Color(int((x % 20)*255/res*((i+j*4) % section < width) + (10-min(x % 20,10))*((i+j*4) % section >= width)),
                                          int((x % 20)*255/res*((i+j*4) % section < width) + (10-min(x % 20,10))*((i+j*4) % section >= width)),
                                          0
                                      ))
            strip.show()
            if shouldstop():
                return
        j+=1


        
# Define functions which animate LEDs in various ways.

def colorWipe(strip, color, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if shouldstop():
            return

def color(strip, color):
    """Go directly to color."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def lavalamp(strip, wait_ms=1):
    """Lava lamp."""
    tick = 122323;
    randx = random.randint(1,5)
    randy = random.randint(1,5)
    randr = random.randint(1,126)
    randb = random.randint(1,126)
    randg = random.randint(1,126)
    while 1:
        randx += random.randint(-1,1)
        if randx <= 0:
            randx =1;
        if randx > 30:
            randx =30;
            
        randy += random.randint(-1,1)
        if randy <= 0:
            randy =1;
        if randy > 30:
            randy =30;

        for i in range(strip.numPixels()):
            y = math.floor(i /16)-LED_HEIGHT/2
            x = (15 * (y % 2)) + (i % 16) * (-2 * (y % 2)+1)-LED_WIDTH/2
            y += 0.5
            x += 0.5
            ps = tick
            s = ps
            myx = (math.sin(math.sqrt(x*x + y*y)/100+s/1000))
            myy = (math.cos(math.sqrt(x*x + y*y)/100+s/1000))

            s  = ps /240

            myx *= (math.sin(math.sqrt(x*x + y*y)/100+s/1000))
            myy *= (math.cos(math.sqrt(x*x + y*y)/100+s/1000))
            if x% 20 == 0: myx = 1.0 
            if y% 20 == 0: myy = 1.0 
            r = myx*(math.sin(x/20+s)+math.cos(s))+myy*(math.sin(s)+math.cos(s))
            g = .5*myy*(math.sin(s)+math.cos(s))+myx*(math.sin(s)+math.cos(s))
            b = myx*math.sin(s)+myy*math.cos(s)
            r = int (-r*255)
            g = int (-g*255)
            b = int (-b*255)
            print r,g,b
            strip.setPixelColor(i, Color(r,g,b))
#            strip.setPixelColor(i, Color( int(brightness*(randr*math.sin((tick+x)/randx)*math.cos((tick+y)/randy)+randr+2)), int(brightness*(randg*math.sin((tick+x)/randx)*math.cos((tick+y)/randy)+randg+2)),int(brightness*(randb*math.sin((tick+x)/randx)*math.cos((tick+y)/randy)+randb+2))));
        strip.show()
        time.sleep(wait_ms/1000.0)
        tick += 1;
        if shouldstop():
            return

def magma(strip, r,g,b, width=16):
    tick = 1
    wait_ms = 20
    while 1:
        for i in range(strip.numPixels()):
            y = math.floor(i /16)-LED_HEIGHT/2;
            x = (15 * (y % 2)) + (i % 16) * (-2 * (y % 2)+1)-LED_WIDTH/2;
            y += 0.5;
            x += 0.5;
            strip.setPixelColor(i, Color( int(r/2*math.sin(tick+x/3)*math.sin(tick+y/3)+r/2),  int(g/2*math.sin(tick+x/3)*math.sin(tick+y/3)+g/2), int(b/2*math.sin(tick+x/3)*math.sin(tick+y/3)+b/2)));
        strip.show()
        time.sleep(wait_ms/1000.0)
        tick += .25
        if shouldstop():
            return

def burner(strip, r,g,b, width=16):
    tick = 1
    direction = 1;
    wait_ms = 20
    while 1:
        for i in range(strip.numPixels()):
            y = math.floor(i /16)-LED_HEIGHT/2;
            x = (15 * (y % 2)) + (i % 16) * (-2 * (y % 2)+1)-LED_WIDTH/2;
            y += 0.5;
            x += 0.5;
            strip.setPixelColor(i, Color( int(-r/2*math.cos(x*x/(32-tick)+y*y/(32-tick))+r/2+1),  int(-g/2*math.cos(x*x/(32-tick)+y*y/(32-tick))+g/2+1), int(-b/2*math.cos(x*x/(32-tick)+y*y/(32-tick))+b/2+1)));
                
        strip.show()
        time.sleep(wait_ms/1000.0)
        tick += direction*.25
        if tick >=31.5:
            direction = -1 
        if tick <=0:
            direction = 1
        if shouldstop():
            return


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            if shouldstop():
                return
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if shouldstop():
            return


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if shouldstop():
            return


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            if shouldstop():
                return
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def shouldstop():
    if os.path.exists("command.txt"):
        return True
    return False

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        print("ready")
        while True:
            if os.path.exists("command.txt"):
                f = open ("command.txt","r")
                if f.mode == "r":
                    contents = f.read()
                    f.close()
                    os.remove("command.txt")
                    if contents.startswith("color") :
                        print ('Color animation')
                        pieces = contents.split()
                        color(strip, Color(int(pieces[2]),int(pieces[1]),int(pieces[3])))  
                    if contents.startswith("brightness") :
                        print ('Set brightness')
                        pieces = contents.split()
                        setbrightness(pieces[1])
                    if contents.startswith("burner") :
                        print ('Burner')
                        pieces = contents.split()
                        burner(strip, int(pieces[2]),int(pieces[1]),int(pieces[3]))
                    if contents.startswith("magma") :
                        print ('Magma')
                        pieces = contents.split()
                        magma(strip, int(pieces[2]),int(pieces[1]),int(pieces[3]))
                    if contents.startswith("candles") :
                        print ('Candle animation')
                        candles(strip, 10, 20)
                    if contents.startswith("chase") :
                        print ('Theatre chase animation')
                        theaterChase(strip, Color(127, 127, 127))
                    if contents.startswith("wipe") :
                        pieces = contents.split()
                        print ('Wipe Candle animation')
                        colorWipe(strip, Color(int(pieces[2]),int(pieces[1]),int(pieces[3])))  # Red wipe
                    if contents.startswith("lavalamp") :
                        pieces = contents.split()
                        print ('Lava Lamp')
                        lavalamp(strip)
                    if contents.startswith("rainbow") :
                        print ('Rainbow animation')
                        rainbowCycle(strip, 20, 100)
                    if contents.startswith("copcar") :
                        print ('Copcar animation')
                        copcar(strip, 20, 4, 100)
                    if contents.startswith("runway") :
                        print ('Runway enterance animation')
                        runway(strip, -1, 4, 1000)
                    if contents.startswith("wheel") :
                        print ('Wheel animation')
                        wheel(200)
                f.close()

#            print ('Color wipe animations.')
#            colorWipe(strip, Color(255, 0, 0))  # Red wipe
#            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#            colorWipe(strip, Color(0, 0, 255))  # Green wipe
#            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            color(strip,Color(0,0,0))
