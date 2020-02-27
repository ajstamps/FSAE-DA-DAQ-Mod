import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE1)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
pin1 = AnalogIn(mcp, MCP.P0)
pin2 = AnalogIn(mcp, MCP.P1)
pin3 = AnalogIn(mcp, MCP.P2)
pin4 = AnalogIn(mcp, MCP.P3)
pin5 = AnalogIn(mcp, MCP.P4)
pin6 = AnalogIn(mcp, MCP.P5)
pin7 = AnalogIn(mcp, MCP.P6)
pin8 = AnalogIn(mcp, MCP.P7)

while True:
    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    sleep(0.1)
