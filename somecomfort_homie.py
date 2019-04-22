#!/usr/bin/env python

import time
import somecomfort

from homie_devices.device_honeywell_thermostat import Device_Honeywell_Thermostat

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mqtt_settings = {
    'MQTT_BROKER' : 'MQTT',
    'MQTT_PORT' : 1883,
}

user = 'email'
password = 'password'

thermostats = {}

client = None

while True:
    try:
        
        client = somecomfort.SomeComfort(user,password)

        for l_name, location in client.locations_by_id.items():
            logging.info('Found Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                logging.info('Found Device %s: %s' % (key, device.name))

                thermostat = Device_Honeywell_Thermostat(device_id=str(key),name = device.name,mqtt_settings=mqtt_settings,tcc_device=device)
                thermostats [key] = thermostat
           
        while True:
            time.sleep(120)
            for key,thermostat in thermostats.items():
                thermostat.update ()


    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

