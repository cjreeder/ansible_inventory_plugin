#!/usr/bin/env python

from _future_ import (absolute_import, division, print_function)
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
import ansible.module_utils.six.moves.urllib.request as urllib_request
import ansible.module_utils.six.moves.urllib.error as urllib_error

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError

class InventoryModule(BaseInventoryPlugin):
    Name = 'couch_inventory'
    
    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin to consume'''
        super(InventoryModule, self).verify_file(path)
        return path.endswith(('couch_inventory.yaml', 'couch_inventory.yml'))

    def device_Designation(l, rooms_location):
        hostname = l  
        print(hostname)
        host_name_split=hostname.split("-")
        building_name = host_name_split[0]
        room_number = host_name_split[1]
        room = host_name_split[0] + '-' + host_name_split[1]
        if buildings[building_name]:
            buildings[building_name].append(hostname)
        else:
            buildings[building_name] = [hostname]

        try:
            room_response = urlopen(rooms_location+room)
            rr=room_response.read()
            rr_json = json.loads(rr)
            desig = rr_json['designation']
        except urllib.error.HTTPError:
            print("Cannot Get designation")
            desig = 'no_designation'

        if desig=='production':
            print(desig)
            production.append(hostname)
        elif desig=='stage':
            stage.append(hostname)
            print(desig)
        else:
            no_designation.append(hostname)
            print(desig)
    
    def couch_inventory(self, devices, rooms):
        try: 
            response = urlopen(devices)
            resp = response.read()
            resp_json = json.loads(resp)
        except urllib.error.HTTPError:
            print("Cannot get information from database")
            return -1
        for row in resp_json["rows"]:
            lists.append(row['id'])


        for l in lists:
            if re.search(r'-CP[0-9]+\b', l):
                CP.append(l)
                device_Designation(l)
            elif re.search(r'-SP[0-9]+\b', l):
                SP.append(l)
                device_Designation(l)
            elif re.search(r'-STB[0-9]+\b', l):
                STB.append(l)
                device_Designation(l)
            elif re.search(r'-MSD[0-9]+\b', l):
                MSD.append(l)
                device_Designation(l)
            elif re.search(r'-DS[0-9]+\b', l):
                DS.append(l)
                device_Designation(l)

        d = {"all": [{"Control Processors":CP},{"Scheduling Panels":SP},{"Set-top Boxes":STB},{"Portable Set-top Boxes":MSD},{"Divider Sensors":DS},{"Production":production},{"Stage":stage},{"No Designation":no_designation},{"Buildings":buildings}]}
        return d 
        #with open('data.txt', 'w') as outfile:
        #    json.dump(d, outfile)

    def parse(self, inventory, loader, path, cache):
        '''Return dynamic inventory from source'''
        super(InventoryModule, self).parse(inventory, loader, path)
    
        # Read the inventory YAML file
        self._read_config_data(path)
    
    try:
        self.plugin = self.get_option('plugin')
        self.dev_url = self.get_option('devices_url')
        self.rm_url = self.get_option('rooms_url')
    except Exception as e:
        raise AnsibleParserError('All correction options required: {}'.format(e))

    self.couch_populate()


    #root_group_name = self.inventoiry.add_group('root_group')

    


