#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_string import Property_String

class Device_Total_Comfort_Account(Device_Base):

    tcc_device = None

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(self,'status','Status','status'))
        self.add_node (node)

        self.account_status = Property_String (node,id='connectionstatus',name='Connection Status',value='Not Connected')
        node.add_property (self.account_status)

        self.last_update = Property_String (node,id='lastupdate',name='Last Update',value='None')
        node.add_property (self.last_update)

        self.device_count = Property_String (node,id='devicecount',name='Device Count',value='None')
        node.add_property (self.device_count)

        self.start()



        
