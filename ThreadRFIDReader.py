# -*- coding:utf-8 -*-

import sys
import threading
import serial
from serial.serialutil import PortNotOpenError

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ThreadRFIDReader(threading.Thread):

    def __init__(self, condition, options):
        threading.Thread.__init__(self, name="RFIDReader")

        self.daemon         = True

        self.debug          = options['debug']
        self.port           = options['serial']['port']
        self.baudrate       = options['serial']['baudrate']
        self.bytesize       = options['serial']['bytesize']
        self.parity         = options['serial']['parity']
        self.stopbits       = options['serial']['stopbits']
        self.timeout        = options['serial']['timeout']
        self.xonxoff        = options['serial']['xonxoff']
        self.rtscts         = options['serial']['rtscts']
        self.dsrdtr         = options['serial']['dsrdtr']
        self.number_lenght  = options['serial']['number_length']

        # Handler to RFID reader
        self.reader = None
        
        # Event which is emited when number is read
        self.condition = condition

        # Configure logger
        self.logger = logging.getLogger(__name__)
        if self.debug==True:
            self.logger.setLevel(logging.DEBUG)

    # Open serial port
    def open(self):
        try:
            self.reader = serial.Serial(
                port        = self.port,
                baudrate    = self.baudrate,
                bytesize    = self.bytesize,
                parity      = self.parity,
                stopbits    = self.stopbits,
                timeout     = self.timeout,
                xonxoff     = self.xonxoff,
                rtscts      = self.rtscts,
                dsrdtr      = self.dsrdtr)
            
            self.logger.debug("Create handler and open serial port")

        except Exception as n:
            self.logger.exception("Error during open serial port!")
            sys.exit(2);

    # Close serial port
    def close(self):
        if self.reader != None:
            self.reader.close()
            self.logger.debug("Close serial port")

    def run(self):
        self.logger.debug("Start " + self.name + " thread")

        while True:
            try:
                # Reset input buffer
                self.reader.reset_input_buffer()
                # Read number from RFID reader
                number = self.reader.read(self.number_lenght).decode("utf-8")

                # See https://docs.python.org/3/library/threading.html#threading.Condition.acquire (end of page)
                with self.condition:
                    # Send signal if read number from RFID reader
                    self.condition.data = number
                    self.condition.notify()

                    self.logger.debug("number: " + number)
            except PortNotOpenError:
                pass
            except Exception as n:
                self.logger.exception("Error in " + self.name + " thread")