import time

import serial, struct


class MSP:
    MessageIDs = {
        "MSP_IDENT": 100,
        "MSP_STATUS": 101,
        "MSP_RAW_IMU": 102,
        "MSP_SERVO": 103,
        "MSP_MOTOR": 104,
        "MSP_RC": 105,
        "MSP_RAW_GPS": 106,
        "MSP_COMP_GPS": 107,
        "MSP_ATTITUDE": 108,
        "MSP_ALTITUDE": 109,
        "MSP_ANALOG": 110,
        "MSP_RC_TUNING": 111,
        "MSP_PID": 112,
        "MSP_BOX": 113,
        "MSP_MISC": 114,
        "MSP_MOTOR_PINS": 115,
        "MSP_BOXNAMES": 116,
        "MSP_PIDNAMES": 117,
        "MSP_WP": 118,
        "MSP_BOXIDS": 119,
        "MSP_SERVO_CONF": 120,

        "MSP_SET_RAW_RC": 200,
        "MSP_SET_RAW_GPS": 201,
        "MSP_SET_PID": 202,
        "MSP_SET_BOX": 203,
        "MSP_SET_RC_TUNING": 204,
        "MSP_ACC_CALIBRATION": 205,
        "MSP_MAG_CALIBRATION": 206,
        "MSP_SET_MISC": 207,
        "MSP_RESET_CONF": 208,
        "MSP_SET_WP": 209,
        "MSP_SELECT_SETTING": 210,
        "MSP_SET_HEAD": 211,
        "MSP_SET_SERVO_CONF": 212,

        "MSP_SET_MOTOR": 214,

        "MSP_BIND": 240,
        "MSP_EEPROM_WRITE": 250
    }

    def __init__(self, port):
        self.port = serial.Serial()
        self.port.port = port
        self.port.baudrate = 115200
        self.port.bytesize = serial.EIGHTBITS
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.timeout = 0
        self.port.xonxoff = False
        self.port.rtscts = False
        self.port.dsrdtr = False
        self.port.writeTimeout = 2

        try:
            self.port.open()
        except Exception as e:
            print(str(e))

    def sendCMD(self, data_len, code, data, data_format):
        crc = 0
        total_data = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), data_len, code] + data
        for i in struct.pack('<2B' + data_format, *total_data[3:len(total_data)]):
            crc = crc ^ i
        total_data.append(crc)
        try:
            b = None
            b = self.port.write(struct.pack('<3c2B' + data_format + 'B', *total_data))
            print(struct.pack('<3c2B' + data_format + 'B', *total_data))
        except Exception as error:
            print("\n\nError sending command:")
            print("(" + str(error) + ")\n\n")
            pass

    def sendRawRC(self, ch_data):
        self.sendCMD(len(ch_data) * 2, MSP.MessageIDs.get("MSP_SET_RAW_RC"), ch_data, str(len(ch_data))+'H')
