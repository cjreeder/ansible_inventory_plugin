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
    Path_to_couchdb_devices:
      description: Web location of the devices for the inventory file 
    Path_to_couchdb_rooms:
      description: Web location of the rooms for the inventory file
      required: true
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError

class InventoryModule(BaseInventoryPlugin):
  Name = 'couch_inventory'

  def verify_file(self, path):
    '''Return true/false if this is possibly a valid file for this plugin to consume
    '''
    pass

  def parse(self, inventory, loader, path, cache):
    '''Return dynamic inventory from source'''
    pass


