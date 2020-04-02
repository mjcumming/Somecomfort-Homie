#!/usr/bin/env python

import somecomfort
import timer3
import sys
import requests
import os
import datetime

from .homie_device.device_honeywell_thermostat import Device_Honeywell_Thermostat
from .homie_device.device_total_comfort_account import Device_Total_Comfort_Account

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

        self.account_device = Device_Total_Comfort_Account(device_id='somecomfort-account',name="Total Comfort Account",homie_settings=self.homie_settings,mqtt_settings=self.mqtt_settings)

        self._connect()

        def update():
            if self.client is None:
                self._connect()
            else:
                self._refresh()

        self.timer = timer3.apply_interval(self.refresh_interval * 60 * 1000, update, priority=0)

    def _connect(self):
        try:
            self.client = somecomfort.SomeComfort(self.username,self.password)
            logging.info('Somecomfort connected to user account {}'.format(self.username))
            self._add_devices() 
            self.account_device.account_status.value="Connected"

        except Exception as exc:
            logging.warning('Somecomfort unable to connect to user account {}, error {}'.format(self.username,exc), exc_info=True)
            self.client = None
            self.account_device.account_status.value="Not Connected to {}  Error {}".format(self.username,exc)

    def _add_devices(self):
        for l_name, location in self.client.locations_by_id.items():
            logging.info('Somecomfort found Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                logging.info('Somecomfort found Device %s: %s' % (key, device.name))
                thermostat = Device_Honeywell_Thermostat(device_id='somecomfort{}'.format(key),name=device.name,homie_settings=self.homie_settings,mqtt_settings=self.mqtt_settings,tcc_device=device)
                self.thermostats [key] = thermostat

        self.account_device.device_count.value=len(self.thermostats)

    def _refresh(self):
        if self.client:
            for _,thermostat in self.thermostats.items():
                try:
                    thermostat.update ()      
                    self.account_device.last_update.value=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                except (
                    somecomfort.client.APIRateLimited,
                    OSError,
                    requests.exceptions.ReadTimeout,
                ) as exp:
                    logging.error("SomeComfort update failed, Retrying - Error: %s", exp)
                    self._connect()
                    self.account_device.last_update.value="Failed {}".format(exp)
                    thermostat.account_status.value="Disconnected {}".format(exp)
        else:
            self._connect()

