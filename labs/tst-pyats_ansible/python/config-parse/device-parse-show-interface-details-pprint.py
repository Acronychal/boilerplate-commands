# credit Hank Preston @ Cisco
# Import our libraries
from genie.conf import Genie
import csv

# Create a testbed object for the network
testbed = Genie.init("testbed.yaml")

# Create an empty dictionary that will hold the details we'll write to the CSV
device_interface_details = {}

# Loop over each device in the network testbed
for device in testbed.devices:
    # Connect to the device
    testbed.devices[device].connect(learn_hostname=True, log_stdout=False)

    # Run the "show interfaces" command on the device
    interface_details = testbed.devices[device].learn("interface")
    #   Note: see available commands to parse for each platform at
    #         https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers
    #   Extra Note: IOS uses "show interfaces" NX-OS uses "show interface"
    #     so the below will work on IOS, but not NX-OS.
    #     A "better option" would be to .learn("interface") which works on
    #     all platforms

    # Store this devices interface details into the dictionary
    device_interface_details[device] = interface_details

# The name for our report file
interface_file = "interfaces.csv"

# The headers we'll use in the CSV file
report_fields = ["Device", "Interface", "MAC Address"]

# Open up the new file for "w"riting
with open(interface_file, "w") as f:
    # Create a CSV "DictWriter" object providing the list of fields
    writer = csv.DictWriter(f, report_fields)
    # Write the header row to start the file
    writer.writeheader()

    # Loop over each device and interface details we gathered and stored
    for device, interfaces in device_interface_details.items():
        # Loop over each interface for the current device in the outer loop
        for interface, details in interfaces.items():
            # Attempt to write a row. If an interface lacks a MAC (ie Loopback)
            # it will raise a "KeyError"
            try:
                writer.writerow(
                    {
                        "Device": device,
                        "Interface": interface,
                        "MAC Address": details["mac_address"],
                    }
                )
            except KeyError:
                # Loopback interfaces lack a mac_address, mark it as "N/A"
                writer.writerow(
                    {"Device": device, "Interface": interface, "MAC Address": "N/A"}
                )