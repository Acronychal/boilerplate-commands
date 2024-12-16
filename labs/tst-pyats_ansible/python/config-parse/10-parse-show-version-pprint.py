
from genie.testbed import load
from pprint import pprint

tb = load('/pyats/sandbox.yaml')

dev1 = tb.devices['CORE-01']
dev1.connect(learn_hostname=True, log_stdout=False)

p1 = dev1.parse('show version')

print(p1)

dev2 = tb.devices['CORE-02']
dev2.connect(learn_hostname=True, log_stdout=False)

p2 = dev2.parse('show version')

print(p2)
