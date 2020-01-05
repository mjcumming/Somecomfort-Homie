#!/usr/bin/env python

import somecomfort
import timer3
import sys
import requests

from .homie_device.device_honeywell_thermostat import Device_Honeywell_Thermostat

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



class Somecomfort_Homie(object):
    
    client = None

    thermostats = {}

    def __init__(self, username=None, password=None, refresh_interval=5, homie_settings=None, mqtt_settings=None):
        assert username
        assert password
        assert mqtt_settings

        self.username = username
        self.password = password
        self.refresh_interval = refresh_interval

        self.homie_settings = homie_settings
        self.mqtt_settings = mqtt_settings

        self._connect()

        def update():
            self._refresh()

        self.timer = timer3.apply_interval(self.refresh_interval * 60 * 1000, update, priority=0)

    def _connect(self):
        try:
            self.client = somecomfort.SomeComfort(self.username,self.password)
            logging.info('Somecomfort connected to user account {}'.format(self.username))
            self._add_devices()
        except:
            logging.info('Somecomfort unable to connect to user account {}, error {}'.format(self.username,sys.exc_info()[0]))
            self.client = None

    def _add_devices(self):
        for l_name, location in self.client.locations_by_id.items():
            logging.info('Somecomfort found Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                logging.info('Somecomfort found Device %s: %s' % (key, device.name))
                thermostat = Device_Honeywell_Thermostat(device_id='somecomfort{}'.format(key),name=device.name,homie_settings=self.homie_settings,mqtt_settings=self.mqtt_settings,tcc_device=device)
                self.thermostats [key] = thermostat

    def _refresh(self):
        for key,thermostat in self.thermostats.items():
            try:
                thermostat.update ()      
            except (
                somecomfort.client.APIRateLimited,
                OSError,
                requests.exceptions.ReadTimeout,
            ) as exp:
                logging.error("SomeComfort update failed, Retrying - Error: %s", exp)
                self._connect()