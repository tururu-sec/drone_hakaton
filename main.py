import time

from MSP import MSP

msp = MSP("COM8")

msp.sendRawRC([1000, 1100, 1200, 1300, 1400])

while True:
    msp.sendRawRC([1000, 1100, 1200, 1300, 1400])
    time.sleep(0.05)