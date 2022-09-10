#!/home/mdl/Projects/workerterminal/workerterminal-venv/bin/python

# -*- coding:utf-8 -*-

from threading import Condition
from  ThreadRFIDReader import ThreadRFIDReader
import pychrome
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ConditionData(Condition):
    def __init__(self) -> None:
        super().__init__()
        self.data = None

conditionData = ConditionData()

###############################################################################

options = {
    'start_url' : 'https://panel-hala.astem.pl',
    'rfid_url'  : 'https://panel-hala.astem.pl/start.php?card_id=',
    'debug'     : True,

    'rfidreader'  : {
        'debug'     : True,
        'serial'    : {
            'port'          : "/dev/ttyUSB0",
            'baudrate'      : 19200,
            'bytesize'      : 8,
            'parity'        : "N",
            'stopbits'      : 1,
            'timeout'       : None,
            'xonxoff'       : False,
            'rtscts'        : False,
            'dsrdtr'        : False,
            'number_length' : 13}}
}

###############################################################################

try:
    # create a browser instance
    browser = pychrome.Browser(url="http://127.0.0.1:9222")

    # create a tab
    tab = browser.new_tab()

    # start the tab
    tab.start()

    # call method
    tab.Network.enable()
    # call method with timeout
    tab.Page.navigate(url=options['start_url'], _timeout=25)
except Exception as n:
    logging.exception("Error open brwoser")

###############################################################################

try:
    thRFIDReader = ThreadRFIDReader(conditionData, options['rfidreader'])
    thRFIDReader.open()
    thRFIDReader.start()
    
    while True:
        with conditionData:
            conditionData.wait()
            tab.Page.navigate(url=options['rfid_url'] + conditionData.data, _timeout=25)

            logging.warning("RFID Number " + conditionData.data)


except KeyboardInterrupt as n:
    pass
finally:
    # Close serial port
    thRFIDReader.close()

    # stop the tab (stop handle events and stop recv message from chrome)
    tab.stop()

    # close tab
    browser.close_tab(tab)