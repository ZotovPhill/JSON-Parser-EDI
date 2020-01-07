import pymysql
import logging
from myconfig import MyConfiguration

"""
Module establish a connection to the MySQL database.
"""


class DBConf:
    def __init__(self):
        self.mc = MyConfiguration.get_config("config.ini")

    def db_connection(self):
        """
        Establish a connection to the MySQL database.
        Constructor for creating a connection to the database.
        Arguments took from config file
        Returns a Connection Object. It takes a number of
        parameters which are database dependent.
        """
        con = pymysql.connect(
            host=self.mc["mysqlDB"]["host"],
            user=self.mc["mysqlDB"]["user"],
            passwd=self.mc["mysqlDB"]["password"],
            db=self.mc["mysqlDB"]["database"],
        )
        logging.info("Connection data received!")
        return con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        """
        Using these methods __enter__ / __exit__ to allows us to
        implement objects which can be used with the WITH statement.
        """
        return self


if __name__ == "__main__":
    db_conf = DBConf()
    db_conf.db_connection()
