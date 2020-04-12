#!/usr/bin/python3
import math
import time

import smbus

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

class GAReader:
    def __init__(self, file_path_and_name):
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68  # This is the address value read via the i2cdetect command
        self.INT_PIN_CFG = 0x37
        self.INT_ENABLE = 0x38

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)
        self.bus.write_byte_data(self.address, self.INT_PIN_CFG, 0x02)
        self.bus.write_byte_data(self.address, self.INT_ENABLE, 0x01)

        self.file_path_and_name = file_path_and_name
        self.outfile = open(self.file_path_and_name, 'w')

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    @staticmethod
    def dist(a, b):
        return math.sqrt((a * a) + (b * b))

    @staticmethod
    def get_y_rotation(x, y, z):
        radians = math.atan2(x, GAReader.dist(y, z))
        return -math.degrees(radians)

    @staticmethod
    def get_x_rotation(x, y, z):
        radians = math.atan2(y, GAReader.dist(x, z))
        return math.degrees(radians)

    def print_csv(self, values):
        line = ""
        for v in values:
            if line != "":
                line += ','
            line += str(v)
        print(line, file=self.outfile)  # Save data to file

    def recv(self):
        while True:
            time.sleep(0.1)
            gyro_xout = self.read_word_2c(0x43)
            gyro_yout = self.read_word_2c(0x45)
            gyro_zout = self.read_word_2c(0x47)
            print("gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131))
            print("gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131))
            print("gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131))

            accel_xout = self.read_word_2c(0x3b)
            accel_yout = self.read_word_2c(0x3d)
            accel_zout = self.read_word_2c(0x3f)
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            print("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
            print("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
            print("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)
            print("x rotation: ", self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            print("y rotation: ", self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            time.sleep(0.5)
