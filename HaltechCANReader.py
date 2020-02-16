from can import *
import os
from threading import Thread
import time


class CANBusReader:
    def __init__(self):
        # This sets up the channel for the can hat to read from
        # os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

        # USED FOR TESTING #
        # os.system("sudo modprobe vcan")
        # os.system("sudo ip link add dev vcan0 type vcan")
        # os.system("sudo ip link set up vcan0")

        # This sets up the reader itself
        self.bus = interface.Bus(channel='can0', bustype='socketcan_native')

        self.file = str(time.strftime("%Y-%m-%d-%H-%M-%S")) + ".csv"

        self.csv_writer = CSVWriter(self.file)

        self.thread = Thread(target=self.on_message_received, daemon=True)
        self.thread.start()

    def on_message_received(self):
        while True:
            msg = self.bus.recv()

            try:
                self.csv_writer.on_message_received(msg)
            except IndexError:
                print(int(msg.arbitration_id, 16))
