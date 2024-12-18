from pyats import topology
from pprint import pprint

# Load the testbed file
testbed = topology.loader.load('/pyats/sandbox.yaml')

# Iterate through each device in the testbed
for device in testbed.devices.values():
    # Connect to the device
    device.connect(learn_hostname=True, log_stdout=False)

    # Execute a command and parse the output
    output = device.parse('show version')

    # Print the parsed output
    pprint(output)

    # Disconnect from the device
    device.disconnect()
