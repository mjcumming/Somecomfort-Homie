#!/usr/bin/env python

import somecomfort
import timer3
import sys
import requests
import os

from .homie_device.device_honeywell_thermostat import Device_Honeywell_Thermostat
import logging
from logging.handlers import TimedRotatingFileHandler

import somecomfort_homie
import homie

logger = logging.getLogger(__name__)

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.path.expanduser("~") + "/somecomforthomie.log"

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)

file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
file_handler.setFormatter(FORMATTER)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logging.basicConfig(level=logging.DEBUG,handlers=[file_handler,console_handler])

HOMIE_SETTINGS = {
    "update_interval": 60,
    "implementation": "Somecomfort Homie {} Homie 4 Version {}".format(
        somecomfort_homie.__version__,homie.__version__
    ),
    "fw_name": "Somecomfort",
    "fw_version": '0.6.0',
}



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
        except Exception as exc:
            logging.warning('Somecomfort unable to connect to user account {}, error {}'.format(self.username,exc), exc_info=True)
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