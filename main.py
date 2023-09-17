import time

from MSP import MSP

msp = MSP("COM4")

msp.sendRawRC([1000, 1500, 1000, 1000, 1000])

while True:
    msp.readGPS()
    time.sleep(1/50)