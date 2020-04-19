import os
from threading import Thread
from can import *


class CANBusReader:
    def __init__(self, file_path_and_name):
        # This sets up the channel for the can hat to read from
        # Further explanation is this:
        # sudo - super user do
        # /sbin/ip - A command for setting up protocols
        # link - add a new link
        # set can0 - set the link name to can0
        # up - make the link online immediately
        # type can - set the link type, we are using a CAN bus so we set it to can
        # bitrate 500000 - how fast the information is coming, 500000 bit/s
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

        # Reader setup
        can_interface = 'can0'
        self.file_path_and_name = file_path_and_name
        self.bus = interface.Bus(can_interface, interface='socketcan')

        self.thread = Thread(target=self.log, daemon=True)

    def log(self):
        # PyCAN comes with built in CAN Writer for CSVs, use that
        with SqliteWriter(self.file_path_and_name) as csv_writer:
            while True:
                msg = self.bus.recv(1)  # Receive message with timeout of 1
                if msg is not None:  # If message is meaningful
                    csv_writer.on_message_received(msg)  # Log message
                else:  # If we didn't receive a message, then CAN is not connected
                    print("Check your wiring! No CAN message received in 1 second! (WHICH AIN'T RIGHT!)")

    def start_thread(self):
        self.thread.start()
