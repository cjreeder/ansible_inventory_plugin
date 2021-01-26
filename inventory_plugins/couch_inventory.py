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

  def parse(self, inventory, loader, path, cache):
    '''Return dynamic inventory from source'''
    super(InventoryModule, self).parse(inventory, loader, path)
    self._read_config_data(path)

    root_group_name = self.inventory.add_group('root_group')




