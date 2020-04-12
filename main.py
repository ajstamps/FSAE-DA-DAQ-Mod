from HaltechCANReader import CANBusReader
from GPSReader import GPSReader
from AnalogReader import AnalogReader
import os.path


SavePath = "/home/pi/data/"
CANFileName = "CAN"
GPSFileName = "GPS"
GAFileName = "GA"
AVIFileName = "AVI"

CompleteCANFileName = os.path.join(SavePath, CANFileName+".csv")
CompleteGPSFileName = os.path.join(SavePath, GPSFileName+".csv")
CompleteGAFileName = os.path.join(SavePath, GAFileName+".csv")
CompleteAVIFileName = os.path.join(SavePath, AVIFileName+".csv")

CANReader = CANBusReader()
GPSReader = GPSReader(GPSFileName)


while True:
    i = 0
