import os
import subprocess
import copy 
import socket
import win32serviceutil

import servicemanager
import win32event
import win32service
import sys
from winreg import *
import winreg

from loggers import logger

# get path from registry stored for the application by the installer

WORKING_DIR = os.path.abspath(__file__)
logger.info(WORKING_DIR) 


ENVIRONMENT = copy.deepcopy(os.environ)


class SalesOrderBookService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SalesOrderBookService"
    _svc_display_name_ = "SALES_ORDER_BOOK_SERVICE"
    _svc_description_ = "Pushes sales order book changes every hour"


    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, *args):
        super().__init__(*args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
    
    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                             servicemanager.PYS_SERVICE_STARTED,
                             (self._svc_name_, ''))
        self.main()

    def start(self):
        logger.info("starting service")

    def stop(self):
        logger.info("stopping service")


    def main(self):
        logger.info("running service")
        subprocess.Popen(['python', 'main.py'], env=ENVIRONMENT)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SalesOrderBookService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SalesOrderBookService)