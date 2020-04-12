import time
import serial
from threading import Thread

PORT = "/dev/ttyS0"
BAUD = 9600

s = serial.Serial(PORT)
s.baudrate = BAUD
s.parity = serial.PARITY_NONE
s.databits = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_ONE
s.timeout = 0  # non blocking mode

s.close()
s.port = PORT
s.open()

# ----- SERIAL PORT READ AND WRITE ENGINE --------------------------------------
line_buffer = ""
rec_buffer = None


class GPSReader:
    def __init__(self, file_path_and_name):
        self.REPORT_RATE = 0.1
        self.date = ""
        self.thread = Thread(target=self.log, daemon=True)
        self.file_path_and_name = file_path_and_name

        self.outfile = open(self.file_path_and_name, 'w')

        self.locked = False
        self.next_report = time.time() + self.REPORT_RATE
        self.date, self.timestamp, self.northing, self.northing_flag, self.easting, self.easting_flag = "", "", "", "", "", ""

    def read_waiting(self):
        """Poll the serial and fill up rec_buffer if something comes in"""
        global rec_buffer
        if rec_buffer is not None:
            return True

        line = self.process_serial()
        if line is not None:
            rec_buffer = line
            return True

        return False

    def read(self):
        """Poll the rec_buffer and remove next line from it if there is a line in it"""
        global rec_buffer

        if not self.read_waiting():
            return None

        rec = rec_buffer
        # print("read:" + rec)
        return rec

    def process_serial(self):
        """Low level serial poll function"""
        global line_buffer

        while True:
            data = s.read(1)
            data = data.decode('utf-8')

            if len(data) == 0:
                return None  # no new data has been received
            data = data[0]

            if data == '\r':
                pass  # strip newline

            elif data == '\n':
                line = line_buffer
                line_buffer = ""
                return line

            else:
                line_buffer += data

    # ----- ADAPTOR ----------------------------------------------------------------

    # This is here, so you can change the concurrency and blocking model,
    # independently of the underlying code, to adapt to how your app wants
    # to interact with the serial port.

    # NOTE: This is configured for non blocking send and receive, but no threading
    # and no callback handling.

    def send_message(self, msg):
        """Send a message to the micro:bit.
            It is the callers responsibility to add newlines if you want them.
        """
        s.write(msg)

    def get_next_message(self):
        """Receive a single line of text from the micro:bit.
            Newline characters are pre-stripped from the end.
            If there is not a complete line waiting, returns None.
            Call this regularly to 'pump' the receive engine.
        """
        result = self.read()
        return result

    def print_csv(self, values):
        line = ""
        for v in values:
            if line != "":
                line += ','
            line += str(v)
        print(line, file=self.outfile)  # Save data to file

    def log(self):
        try:
            while True:
                now = time.time()

                if now > self.next_report:
                    self.next_report = now + self.REPORT_RATE
                    values = self.date, self.timestamp, self.locked, self.northing, \
                             self.northing_flag, self.easting, self.easting_flag

                    self.print_csv(values)

                gps_data = self.get_next_message()
                if gps_data is not None:
                    parts = gps_data.split(',')
                    rec_type = parts[0]
                    if rec_type == "$GPRMC":
                        date = parts[9]
                    if rec_type == "$GPGSA":
                        lock_flag = parts[1]
                        if lock_flag == 'A':
                            # print("GPS LOCKED")
                            locked = True
                        else:
                            # print("NO GPS LOCK:%s" % lock_flag)
                            locked = False

                    elif rec_type == "$GPGGA":
                        if locked:
                            self.timestamp, self.northing, self.northing_flag, self.easting, self.easting_flag = parts[
                                                                                                                 1:6]
                        else:
                            self.timestamp, self.northing, self.northing_flag, self.easting, self.easting_flag = "", "", "", "", ""

        except KeyboardInterrupt:
            # Catch keyboard interrupt
            self.outfile.close()
            # os.system("sudo /sbin/ip link set can0 down")
            print('\n\rKeyboard interrupt')
