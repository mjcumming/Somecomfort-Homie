#!/usr/bin/env python

import time
import yaml 

from somecomfort_homie import Somecomfort_Homie

with open("./etc/somecomfort_homie.yml", 'r') as ymlfile:
    cfg = yaml.full_load(ymlfile)

try:
    
    sch = Somecomfort_Homie(username=cfg['somecomfort'] ['username'],password=cfg['somecomfort'] ['password'],mqtt_settings=cfg['mqtt'])
    
    while True:
        time.sleep(10)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")     