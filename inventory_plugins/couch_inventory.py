#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
_metaclass_ = type

DOCUMENTATION = r'''
  name: couch_inventory
  plugin_type: inventory
  short_description: Returns Ansible inventory from a couch database
  description: Plugin that returns a JSON ansible inventory from a couch database in the yaml configuration file.
  options:
    plugin:
      description: Name of the plugin
      required: true
      choices: ['couch_inventory']
    devices_url:
      description: Web location of the devices for the inventory file
      required: true
    rooms_url:
      description: Web location of the rooms for the inventory file
      required: true
'''
from urllib.request import urlopen
import urllib.error
import json
import socket
import re

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError

from collections import defaultdict

lists = []
CP = []
SP = []
STB = []
MSD = []
DS = []
TC = []
production = []
stage = []
no_designation = []
buildings = []

class InventoryModule(BaseInventoryPlugin):
    Name = 'couch_inventory'
    
    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin to consume'''
        super(InventoryModule, self).verify_file(path)
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('couch_inventory.yaml', 'couch_inventory.yml')):
                valid = True
        return valid

    def device_Designation(self, l, rooms_resp):
        hostname = l  
        host_name_split=hostname.split("-")
        building_name = host_name_split[0]
        room_number = host_name_split[1]
        room = host_name_split[0] + '-' + host_name_split[1]
        if building_name not in buildings:
            self.inventory.add_group(building_name)
            buildings.append(building_name)
        self.inventory.add_host(host=hostname, group=building_name)
        
        try:
            res = next((item for item in room_resp['docs'] if item['_id'] == room), None)
            desig = res['designation']
        except TypeError:
            desig = 'no_designation'
        
        if desig=='production':
            self.inventory.add_host(host=hostname, group=desig)
        elif desig=='stage':
            self.inventory.add_host(host=hostname, group=desig)
        else:
            self.inventory.add_host(host=hostname, group="no_designation")
    
    def couch_inventory(self, devices_url, rooms_url):
        self.inventory.add_group('CP')
        self.inventory.add_group('SP')
        self.inventory.add_group('STB')
        self.inventory.add_group('MSD')
        self.inventory.add_group('DS')
        self.inventory.add_group('production')
        self.inventory.add_group('stage')
        self.inventory.add_group('no_designation')
        
        #Get the rooms from the couch database
        body = {
           "selector": {
                "_id": {"$regex": "[A-Z]"}
            },
            "fields": ["_id","designation"],
            "limit": 2000
        }
        body = bytes((json.dumps(body)), 'utf8')
        req = urllib.request.Request(url=rooms_url,data=body,method='POST')
        req.add_header('Content-Type', 'application/json')
        f = urllib.request.urlopen(req)
        resp = f.read()
        room_resp = json.loads(resp)
        
        #Get the Devices from the couch database
        try: 
            response = urllib.request.urlopen(self.devices_url)
            resp = response.read()
            resp_json = json.loads(resp)
        except urllib.error.HTTPError:
            print("Cannot get information from database")
            return -1
        
        for row in resp_json["rows"]:
            lists.append(row['id'])
        
        for l in lists:
            if re.search(r'-CP[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='CP')
            elif re.search(r'-SP[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='SP')
            elif re.search(r'-STB[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='STB')
            elif re.search(r'-MSD[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='MSD')
            elif re.search(r'-DS[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='DS')
            elif re.search(r'-TC[0-9]+\b', l):
                self.device_Designation(l, rooms_resp)
                self.inventory.add_host(host=l, group='TC')
       
    def parse(self, inventory, loader, path, cache):
        '''Return dynamic inventory from source'''
        super(InventoryModule, self).parse(inventory, loader, path)
    
        # Read the inventory YAML file
        self._read_config_data(path)
    
        try:
            self.plugin = self.get_option('plugin')
            self.devices_url = self.get_option('devices_url')
            self.rooms_url = self.get_option('rooms_url')
        except Exception as e:
            raise AnsibleParserError('All correction options required: {}'.format(e))

        self.couch_inventory(self.devices_url, self.rooms_url)


    


