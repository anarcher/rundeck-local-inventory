#!/usr/bin/env python


'''
Rundeck local command env based inventory script for Ansible, in Python.
'''

import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json

class Inventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
                                 
        if self.args.list:
            self.inventory = self.get_inventory()
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()
        print json.dumps(self.inventory);

    def get_inventory(self):
        group_name = os.environ.get('RD_NODE_NAME','group')
        ip = os.environ.get('RD_NODE_IP')
        ssh_user = os.environ.get('RD_NODE_USERNAME','ubuntu')
        ssh_private_key_file = os.environ.get('RD_PRIVATE_KEY_NAME',None)
        data = {
            group_name: {
                'hosts' : [ ip ],
                'vars' : {
                    'ansible_ssh_user' : ssh_user,
                }
            },
            '_meta': {
                'hostvars': {
                    ip : {},
                }
            }
        }
        if ssh_private_key_file:
            data[group_name]['vars']['ansible_ssh_private_key_file'] = ssh_private_key_file
        return data

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}



    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()


if __name__ == '__main__':
    Inventory()

