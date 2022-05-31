#!/usr/bin/python

DOCUMENTATION = '''
---
module: check_disks
short_description: Check if disks have existing LVM/ MDRAID or partitions
'''

EXAMPLES = '''
- name: Check if any of the disks have partitions or data present
  check_disks:
    disks: [ 'sda', 'sdb', 'sdc', 'sde' ]
    excludes: [ 'sde' ]
  register: disk_status
- name: Check all drives for existing partitions
  debug:
    msg: 'The disk has existing partitions or data'
  when: disk_status.status
'''

from ansible.module_utils.basic import *
import subprocess
import re

def main():

    # Data we can pass in to the module
    fields = {
        "disks": {"required": True, "type": "list"},
        "excludes": {
            "default": [''],
            "type": 'list'
        },
    }

    # Pull in module fields and pass into variables
    module = AnsibleModule(argument_spec=fields)
    disks = module.params['disks']
    excludes = module.params['excludes']

    # Check disks for existing partitions
    status, status_string = check_partitions(disks, excludes)

    # Return if the disks are safe to write to or not
    module.exit_json(changed=False, status=status, output=status_string)


def check_partitions(disks, excludes):

    # Update disks to remove any excludes in the exclude list, this is based on a string match so md will match md-1 or md1 etc
    for exclude in excludes:
        disks = [s for s in disks if exclude not in s]

    # Iterate over the remaining disks
    for disk in disks:
        # Check for existing partitions
        command = [ 'ls /dev/' + disk + '[0-9]' ]
        runcommand = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = runcommand.communicate()
        if runcommand.returncode == 0:
            return True, ('Found partition on ' + disk)

        # Check for existing mdraid
        with open('/proc/mdstat', 'r') as mdraid_status:
            mdraid_status = mdraid_status.read()
        if re.search( disk, mdraid_status ):
            return True, ('Found mdraid on ' + disk)

        # Check for existing LVM ( PVs )
        command = [ 'pvs' ]
        runcommand = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = runcommand.communicate()
        if re.search( '/dev/' + disk, stdout.decode() ):
            return True, ('Found pvs on ' + disk)

    return False, ('No Partitions Found')

if __name__ == '__main__':
    main()
