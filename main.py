from HaltechCANReader import CANBusReader
from GPSReader import GPSReader
from AnalogReader import AnalogReader
from GAReader import GAReader
import os
import signal
import sys
import time
import threading
import logging

# Where the data gets stored
SavePath = "/home/pi/data/"

# The specific directory, based on time
SavePath += str(time.strftime("%Y-%m-%d-%H-%M-%S")) + "/"

# All the filenames
CANFileName = "CAN"
GPSFileName = "GPS"
GAFileName = "GA"
AVIFileName = "AVI"

# Complete the full filenames
CompleteCANFileName = os.path.join(SavePath, CANFileName + ".csv")
CompleteGPSFileName = os.path.join(SavePath, GPSFileName + ".csv")
CompleteGAFileName = os.path.join(SavePath, GAFileName + ".csv")
CompleteAVIFileName = os.path.join(SavePath, AVIFileName + ".csv")

# Check if the path exists (it shouldn't, time should be going forwards)
if not os.path.exists(SavePath):
    os.mkdir(SavePath)

# Set as working directory
os.chdir(SavePath)

# Print current working directory
cwd = os.getcwd()
print(cwd)

# Logging for debugging purposes
logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# CANReader = CANBusReader(CompleteCANFileName)
GPSReader = GPSReader(CompleteGPSFileName)
GAReader = GAReader(CompleteGAFileName)

AVIReader = AnalogReader(CompleteAVIFileName)


def signal_handler(signal, frame):
    sys.exit(0)


def main():
    # CANReader.start_thread()
    GPSReader.start_thread()
    GAReader.start_thread()
    AVIReader.start_thread()
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    forever = threading.Event()
    forever.wait()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("Exception Occurred", exc_info=True)
