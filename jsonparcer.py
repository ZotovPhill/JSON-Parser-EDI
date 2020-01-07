import time
import logging

from parcerservice import Parcerservice
from dbconf import DBConf
from dataparcer import DataParcer
from parcerfunction import ParcerFunction
from myconfig import MyConfiguration

"""
Main Service Module. Control EDI module, that runs
Windows Service in background for parsing data from JSON
file and inserting them to database.
"""


class PythonJsonParcer(Parcerservice):
    _svc_name_ = "PythonJsonParcer"
    _svc_display_name_ = "Python Json Parcer Service"
    _svc_display_name_ = "Hope this will be work"

    def start(self):
        """
        Initializing variables, creating instances of a classes,
        before running the main loop of a service.
        """
        self.mc = MyConfiguration.get_config("config.ini")

        logging.basicConfig(
            filename=self.mc["Path"]["log_file"],
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.db_settings = DBConf()
        # Recieve a Connection Object for database processing
        self.db_connect = self.db_settings.db_connection()
        file_path = self.mc["Path"]["work_dir"]
        # Json file parser, collecting data and checkup
        self.data_parcer = DataParcer(file_path)
        self.parcer_function = ParcerFunction(self.db_connect)
        # Check if 'calling' table is exist, otherwise create it
        self.parcer_function.create_table()

        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):

        while self.isrunning:
            ed = self.data_parcer.extract_data()

            for item in ed:
                # Take data from record dictionary for next processing
                first_number, second_number, start_call, end_call, connection_type = [
                    v[1] for v in item.items()
                ]
                # Fetch data about cost per/min for each record
                type_cost = self.parcer_function.execute_connection_type(
                    start_call, end_call, connection_type
                )
                # Calculating cost for each record
                cost = self.parcer_function.calculate_cost(
                    start_call, end_call, type_cost
                )
                # Opening connection and Inserting to Database
                self.parcer_function.insert_data(
                    first_number, second_number, start_call, end_call, cost
                )
            time.sleep(5)


if __name__ == "__main__":
    PythonJsonParcer.parce_command_line()
