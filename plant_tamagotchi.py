#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from epd import epd2in13bc
from grove_moisture_sensor import GroveMoistureSensor
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def draw(epd, status):
    try:
        # logging.info("epd2in13bc Demo")
        
        # epd = epd2in13bc.EPD()
        # logging.info("init and Clear")
        epd.init()
        # epd.Clear()
        # time.sleep(1)
        
        # # Drawing on the image
        # logging.info("Drawing")    
        # font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
        # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        # # Drawing on the Horizontal image
        # logging.info("1.Drawing on the Horizontal image...") 
        # HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        # HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
        # drawblack = ImageDraw.Draw(HBlackimage)
        # drawry = ImageDraw.Draw(HRYimage)
        # drawblack.text((10, 0), 'hello world', font = font20, fill = 0)
        # drawblack.text((10, 20), '2.13inch e-Paper bc', font = font20, fill = 0)
        # drawblack.text((120, 0), u'微雪电子', font = font20, fill = 0)    
        # drawblack.line((20, 50, 70, 100), fill = 0)
        # drawblack.line((70, 50, 20, 100), fill = 0)
        # drawblack.rectangle((20, 50, 70, 100), outline = 0)    
        # drawry.line((165, 50, 165, 100), fill = 0)
        # drawry.line((140, 75, 190, 75), fill = 0)
        # drawry.arc((140, 50, 190, 100), 0, 360, fill = 0)
        # drawry.rectangle((80, 50, 130, 100), fill = 0)
        # drawry.chord((85, 55, 125, 95), 0, 360, fill =1)
        # epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        # time.sleep(2)
        
        # # Drawing on the Vertical image
        # logging.info("2.Drawing on the Vertical image...")
        # LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 126*298
        # LRYimage = Image.new('1', (epd.width, epd.height), 255)  # 126*298
        # drawblack = ImageDraw.Draw(LBlackimage)
        # drawry = ImageDraw.Draw(LRYimage)
        
        # drawblack.text((2, 0), 'hello world', font = font18, fill = 0)
        # drawblack.text((2, 20), '2.13 epd b', font = font18, fill = 0)
        # drawblack.text((20, 50), u'微雪电子', font = font18, fill = 0)
        # drawblack.line((10, 90, 60, 140), fill = 0)
        # drawblack.line((60, 90, 10, 140), fill = 0)
        # drawblack.rectangle((10, 90, 60, 140), outline = 0)
        # drawry.rectangle((10, 150, 60, 200), fill = 0)
        # drawry.arc((15, 95, 55, 135), 0, 360, fill = 0)
        # drawry.chord((15, 155, 55, 195), 0, 360, fill =1)
        # epd.display(epd.getbuffer(LBlackimage), epd.getbuffer(LRYimage))
        # time.sleep(2)
        
        # logging.info("3.read bmp file")
        # HBlackimage = Image.open(os.path.join(picdir, '2in13bc-b.bmp'))
        # HRYimage = Image.open(os.path.join(picdir, '2in13bc-ry.bmp'))
        # epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        # time.sleep(2)
        
        logging.info("4.read bmp file on window")
        blackimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
        plant = Image.open(os.path.join(picdir, status + '.png'))
        rotated = plant.transpose(Image.ROTATE_90)
        width, height = rotated.size
        enlarged = rotated.resize((width * 4, height * 4))
        new_width, new_height = enlarged.size
        blackimage1.paste(enlarged, (round((epd.height - new_width) / 2), round((epd.width - new_height) / 2)))
        epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))
        
        # logging.info("Clear...")
        # epd.init()
        # epd.Clear()
        
        logging.info("Goto Sleep...")
        epd.sleep()
        # time.sleep(3)
        # epd.Dev_exit()
            
    # except IOError as e:
    #     logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in13bc.epdconfig.module_exit()
        exit()
        
def get_moisture_status(status, sensor):
    moisture = sensor.moisture
    if status == None:
        if moisture > 1900:
            return (moisture, 'dry')
        elif moisture > 1500:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'dry':
        if moisture > 1850:
            return (moisture, 'dry')
        elif moisture > 1500:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'moist':
        if moisture > 1950:
            return (moisture, 'dry')
        elif moisture > 1450:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'wet':
        if moisture > 1900:
            return (moisture, 'dry')
        elif moisture > 1550:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
        
SHORT_DELAY = 15
LONG_DELAY = 180

def is_too_many_updates(recent_intervals):
    return len(recent_intervals) > 5 and sum(recent_intervals) / len(recent_intervals) < LONG_DELAY
        

def main():
    epd = epd2in13bc.EPD()
    
    sensor = GroveMoistureSensor(0)
    draw_delay = SHORT_DELAY
    recent_intervals = []
    last_moisture_status = None
    last_screen_update = None
    
    while 1:
        (moisture, status) = get_moisture_status(last_moisture_status, sensor)
        now = time.time()
        
        logging.info("time: {0}".format(now))
        logging.info("moisture level: {0}".format(moisture))
        logging.info("last update: {0}".format(last_screen_update))
        logging.info("previous status: {0}".format(last_moisture_status))
        logging.info("current status: {0}".format(status))
        logging.info("last update times: {0}".format(recent_intervals))
        logging.info("draw delay: {0}".format(draw_delay))
        if last_moisture_status == None or last_screen_update == None:
            last_screen_update = now
            last_moisture_status = status
            draw(epd, status)
        elif last_moisture_status != status and now - last_screen_update > draw_delay:
            if draw_delay < SHORT_DELAY:
                recent_intervals.append(now - last_screen_update)
                recent_intervals = recent_intervals[-10:]
                draw_delay = draw_delay * 2
            else:
                recent_intervals = []
            last_screen_update = now
            last_moisture_status = status
            if (is_too_many_updates(recent_intervals)):
                draw_delay = LONG_DELAY
            else:
                draw_delay = SHORT_DELAY
            draw(epd, status)
        time.sleep(5)

main()
