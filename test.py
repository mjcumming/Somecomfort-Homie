#!/usr/bin/env python

import time

from somecomfort_homie import Somecomfort_Homie

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}

     
try:

    sch = Somecomfort_Homie(username='mike@4831.com',password='Minaki17',mqtt_settings=mqtt_settings)
    
    while True:
        time.sleep(10)


except (KeyboardInterrupt, SystemExit):
    print("Quitting.")        
