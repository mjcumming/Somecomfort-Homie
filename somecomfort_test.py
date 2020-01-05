#!/usr/bin/env python

import time
import somecomfort
import timer3
import sys
import requests

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



class Somecomfort_Homie(object):
    
    client = None

    thermostats = {}

    def __init__(self, username=None, password=None, refresh_interval=3):
        assert username
        assert password

        self.username = username
        self.password = password
        self.refresh_interval = refresh_interval

        self.devices={}

        self._connect()

        def update():
            self._refresh()

        self.timer = timer3.apply_interval(self.refresh_interval * 60 * 1000, update, priority=0)

    def _connect(self):
        try:
            self.client = somecomfort.SomeComfort(self.username,self.password)
            logging.info('Somecomfort connected to user account {}'.format(self.username))
            self._add_devices()
            return True
        except:
            logging.warning('Somecomfort unable to connect to user account {}, error {}'.format(self.username,sys.exc_info()[0]))
            self.client = None
            return False

    def _add_devices(self):
        for l_name, location in self.client.locations_by_id.items():
            logging.info('Somecomfort found Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                logging.info('Somecomfort found Device %s: %s' % (key, device.name))
                device.refresh()
                print('Device {}'.format(device.raw_ui_data))
                print('Device {}'.format(device.raw_fan_data))
                print('Device {}'.format(device.raw_dr_data))
                self.devices [key] = device
                #self._print_device(device)

    def _refresh(self):
        print ("REFRESH")
        for key,device in self.devices.items():
            try:
                print ("Alive",device.is_alive)
                device.refresh ()      
            except (
                somecomfort.client.APIRateLimited,
                OSError,
                requests.exceptions.ReadTimeout,
            ) as exp:
                logging.error("SomeComfort update failed, Retrying - Error: %s", exp)
                self._connect()


    def _print_device(self,device):
        print (device.raw_ui_data)


if __name__ == "__main__":

    try:
        c = Somecomfort_Homie(username='mike@4831.com',password='Minaki17')

        while True:
            time.sleep(2)


    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
