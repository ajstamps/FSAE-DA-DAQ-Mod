import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from threading import Thread

class AnalogReader:
    def __init__(self, file_and_path_name):
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.CE1)
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        self.file_path_and_name = file_and_path_name

        self.pin1 = AnalogIn(self.mcp, MCP.P0)
        self.pin2 = AnalogIn(self.mcp, MCP.P1)
        self.pin3 = AnalogIn(self.mcp, MCP.P2)
        self.pin4 = AnalogIn(self.mcp, MCP.P3)
        self.pin5 = AnalogIn(self.mcp, MCP.P4)
        self.pin6 = AnalogIn(self.mcp, MCP.P5)
        self.pin7 = AnalogIn(self.mcp, MCP.P6)
        self.pin8 = AnalogIn(self.mcp, MCP.P7)

        self.outfile = open(self.file_path_and_name, 'w')

        self.thread = Thread(target=self.read, daemon=True)

    def read(self):
        while True:
            self.print_csv([self.pin1.value, self.pin2.value,
                            self.pin3.value, self.pin4.value,
                            self.pin5.value, self.pin5.value,
                            self.pin6.value, self.pin8.value])

    def print_csv(self, values):
        line = ""
        for v in values:
            if line != "":
                line += ','
            line += str(v)
        print(line, file=self.outfile)  # Save data to file
