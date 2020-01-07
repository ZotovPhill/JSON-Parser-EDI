import socket

import win32serviceutil

import servicemanager
import win32event
import win32service

import logging


class Parcerservice(win32serviceutil.ServiceFramework):
    """
    Base class to create Windows Service
    """

    _svc_name_ = "pythonService"
    _svc_display_name_ = "Python Service"
    _svc_description_ = "Python Service Description"

    @classmethod
    def parce_command_line(cls):
        """
        Method to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the Service
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        logging.critical("SERVICE PythonJsonParcer HAS BEEN STOPPED!")

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        logging.critical("SERVICE PythonJsonParcer HAS BEEN STARTED!")
        self.main()

    def start(self):
        """
        Override...Do something when the
        service is starting (before started)
        """
        pass

    def stop(self):
        """
        Override...Do something when the
        service is stopping (before stopped)
        """
        pass

    def main(self):
        """
        Override...
        Method that will contain the main logic of service
        A loop that keeps alive until the service is stopped.
        Parce files and processed them each 5 seconds.
        """
        pass


if __name__ == "__main__":
    Parcerservice.parce_command_line()
