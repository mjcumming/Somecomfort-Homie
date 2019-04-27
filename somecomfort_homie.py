#!/usr/bin/env python

import time
import somecomfort
import timer3

from homie_device.device_honeywell_thermostat import Device_Honeywell_Thermostat

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


MQTT_SETTINGS = {
    'MQTT_BROKER' : None,
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : None,
}

HOMIE_SETTINGS = {
    'version' : '3.0.1',
    'topic' : 'homie', 
    'fw_name' : 'somecomfort',
    'fw_version' : '0.0.1', 
    'update_interval' : 60, 
    'implementation' : 'HomieV3', 
}


class Somecomfort_Homie(object):
    
    client = None

    thermostats = {}

    def __init__(self, username=None, password=None, refresh_interval=3, homie_settings=HOMIE_SETTINGS, mqtt_settings=None):
        assert username
        assert password
        assert mqtt_settings

        self.username = username
        self.password = password
        self.refresh_interval = refresh_interval

        self.homie_settings = homie_settings
        self.mqtt_settings = mqtt_settings

        def update():
            self._refresh()

        self.timer = timer3.apply_interval(self.refresh_interval * 60 * 1000, update, priority=0)

        self._connect()

    def _connect(self):
        try:
            self.client = somecomfort.SomeComfort(self.username,self.password)
            self._add_devices()
        except:
            self.client = None

    def _add_devices(self):
        for l_name, location in self.client.locations_by_id.items():
            logging.info('Found Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                logging.info('Found Device %s: %s' % (key, device.name))
                thermostat = Device_Honeywell_Thermostat(device_id=str(key),name=device.name,homie_settings=self.homie_settings,mqtt_settings=self.mqtt_settings,tcc_device=device)
                self.thermostats [key] = thermostat

    def _refresh(self):
        if self.client:
            for key,thermostat in self.thermostats.items():
                thermostat.update ()      
        else:
            self._connect()  

