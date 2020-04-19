import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from threading import Thread
import logging
import time


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

        self.outfile = open(self.file_path_and_name, 'a')

        self.thread = Thread(target=self.read, daemon=True)

    def print_csv(self, values):
        line = ""
        for v in values:
            if line != "":
                line += ','
            line += str(v)
        self.outfile.write(line)

    def read(self):
        self.print_csv(["timestamp", "AVI1", "AVI2",
                        "AVI3", "AVI4", "AVI5",
                        "AVI6", "AVI7", "AVI8"])
        try:
            while True:
                self.print_csv([time.time(), self.pin1.voltage, self.pin2.voltage,
                                self.pin3.voltage, self.pin4.voltage, self.pin5.voltage,
                                self.pin5.voltage, self.pin6.voltage, self.pin8.voltage])
                self.outfile.flush()
        except Exception as e:
            logging.error("Error Occurred", exc_info=True)

    def start_thread(self):
        self.thread.start()
