import os
from threading import Thread
import time
from can import *


class CANBusReader:
    def __init__(self):
        # This sets up the channel for the can hat to read from
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

        # USED FOR TESTING #
        # os.system("sudo modprobe vcan")
        # os.system("sudo ip link add dev vcan0 type vcan")
        # os.system("sudo ip link set up vcan0")

        # This sets up the reader itself
        can_interface = 'can0'
        self.bus = interface.Bus(can_interface, interface='socketcan')

        self.file = str(time.strftime("%Y-%m-%d-%H-%M-%S")) + ".csv"

        self.quit = False

        self.thread = Thread(target=self.on_message_received, daemon=True)
        self.thread.start()

    def on_message_received(self):
        with CSVWriter(self.file) as csv_writer:
            try:
                while True:
                    msg = self.bus.recv(1)
                    if msg is not None:
                        csv_writer.on_message_received(msg)
                    else:
                        print("Check your wiring! No CAN message received in 1 second! (WHICH AIN'T RIGHT!)")

            except KeyboardInterrupt:
                pass  # exit normally, happens from time to time
