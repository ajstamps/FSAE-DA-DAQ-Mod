#!/usr/bin/python3
# GPS logger example
# For use with PiCAN-GPS board
# http://skpang.co.uk/catalog/pican-with-gps-canbus-board-for-raspberry-pi-23-p-1520.html
#
# Serial and GPS routine writern by David Whale
#
# SK Pang 15th March 2017
#
#

import time
import serial
from threading import Thread

# ----- SERIAL PORT READ AND WRITE ENGINE --------------------------------------
line_buffer = ""
rec_buffer = None


def read_waiting(s):
    """Poll the serial and fill up rec_buffer if something comes in"""
    global rec_buffer
    if rec_buffer is not None:
        return True

    line = process_serial(s)
    if line is not None:
        rec_buffer = line
        return True

    return False


def read(s):
    """Poll the rec_buffer and remove next line from it if there is a line in it"""
    global rec_buffer

    if not read_waiting(s):
        return None

    rec = rec_buffer
    rec_buffer = None

    return rec


def process_serial(s):
    """Low level serial poll function"""
    global line_buffer

    while True:
        data = s.read(1)
        data = data.decode('utf-8')
        # print(data, type(data), len(data))

        if len(data) == 0:
            # print("RETURN NONE")
            return None  # no new data has been received
        data = data[0]

        if data == '\r':
            # print("RETURN ")
            pass  # strip newline

        elif data == '\n':
            # print("NEWLINE ")
            line = line_buffer
            line_buffer = ""
            # print(line)
            return line

        else:
            # print("ADD %s" % data)
            line_buffer += data


# ----- ADAPTOR ----------------------------------------------------------------

# This is here, so you can change the concurrency and blocking model,
# independently of the underlying code, to adapt to how your app wants
# to interact with the serial port.

# NOTE: This is configured for non blocking send and receive, but no threading
# and no callback handling.

def get_next_message(s):
    """Receive a single line of text from the micro:bit.
        Newline characters are pre-stripped from the end.
        If there is not a complete line waiting, returns None.
        Call this regularly to 'pump' the receive engine.
    """
    return read(s)


class GPSReader:
    def __init__(self, file_path_and_name):
        self.file_and_path_name = file_path_and_name
        self.outfile = open(self.file_and_path_name, 'a')

        self.thread = Thread(target=self.log, daemon=True)

    def print_csv(self, values):
        line = ""
        for v in values:
            if line != "":
                line += ','
            line += str(v)
        line += '\n'
        self.outfile.write(line)  # Save data to file

    def log(self):
        port = "/dev/ttyS0"
        baud = 9600

        s = serial.Serial(port)
        s.baudrate = baud
        s.parity = serial.PARITY_NONE
        s.databits = serial.EIGHTBITS
        s.stopbits = serial.STOPBITS_ONE
        s.timeout = 0  # non blocking mode

        s.close()
        s.port = port
        s.open()

        report_rate = 0.1

        next_report = time.time() + report_rate

        locked = False
        date, timestamp, north, north_flag, easting, easting_flag = "", "", "", "", "", ""
        self.print_csv(["timestamp",
                        "north", "north_flag",
                        "easting", "easting_flag"])
        try:
            while True:
                now = time.time()

                # Get the GPS data
                gps_data = get_next_message(s)
                if gps_data is not None:  # If anything is in there, we go
                    parts = gps_data.split(',')  # Split it into an array
                    rec_type = parts[0]  # This is the GPS message check
                    if rec_type == "$GPRMC":  # This one is basic data that we already have
                        date = parts[9]
                    if rec_type == "$GPGSA":  # This one is information on satellite availability
                        lock_flag = parts[1]
                        if lock_flag == 'A':  # Check if locked
                            locked = True
                        else:
                            locked = False
                    # This is the real meat and potatoes
                    elif rec_type == "$GPGGA":  # Grab GPS data we care about
                        if locked:
                            timestamp, north, north_flag, easting, easting_flag = parts[1:6]
                        else:  # If we lost connection, reset everything
                            timestamp, north, north_flag, easting, easting_flag = "", "", "", "", ""

                    if now > next_report and north != "":
                        next_report = now + report_rate
                        self.print_csv([time.time(),
                                        north, north_flag,
                                        easting, easting_flag])
                        self.outfile.flush()

        finally:
            self.outfile.close()

    def start_thread(self):
        self.thread.start()
