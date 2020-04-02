#!/usr/bin/env python

import time
import yaml 

from somecomfort_homie.somecomfort_homie import Somecomfort_Homie

def start ():

    with open("somecomfort_homie.yml", 'r') as ymlfile:
        cfg = yaml.full_load(ymlfile)

    try:
        
        sch = Somecomfort_Homie(username=cfg['somecomfort'] ['username'],password=cfg['somecomfort'] ['password'],mqtt_settings=cfg['mqtt'])
        
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")     


if __name__ == "__main__":
    start()    