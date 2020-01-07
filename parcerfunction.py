import math
import logging

"""
Module of functions that makes a huge part of base logic
of a EDI, calculating cost and two base methods for
working with database. Logging info check call of methods.
"""


class ParcerFunction:
    def __init__(self, db_connect):
        self.db_connect = db_connect

    def calculate_cost(self, start_call, end_call, type_cost):
        # math.ceil rounds up ( if 1:01 -> 2:00)
        result = (math.ceil((end_call - start_call) / 60)) * type_cost
        return result

    def execute_connection_type(self, start_call, end_call, connection_type):
        """
        The method extracts from the table the cost of a minute for a
        particular type of connection, comparing it with the type of
        connection in things. Price per minute of conversation
        (in indivisible units, it may just be a positive integer).
        """
        with self.db_connect as cursor:
            cursor.execute("SELECT * FROM link")
            # fetchAll() method retrieves all rows of a query result
            link_data = cursor.fetchall()
            for link_row in link_data:
                if link_row[0] == connection_type:
                    return link_row[1]

    def insert_data(self, first_number, second_number, start_call, end_call, cost):
        """
        This is the method that inser data to calling database table.
        Calling for every inserting json item.
        Using SQL query, through mysql cursor connector to database.
        """
        with self.db_connect as cursor:
            cursor.execute(
                "INSERT INTO calling \
                (First_number, Second_number, Start_call, End_call, Cost) \
                VALUES (%s,	%s,	%s, %s, %s)",
                (first_number, second_number, start_call, end_call, cost,),
            )
        logging.info("Data inserted in table")

    def create_table(self):
        """
        This is the method that creates a table of calls if it not found
        in working database, otherwise it throws a warning in cmd that
        table already exist. Using SQL query, through mysql cursor connector
        to database.
        """
        with self.db_connect as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS calling \
                (Call_Id INT(11) NOT NULL AUTO_INCREMENT, \
                    First_number VARCHAR(20), \
                    Second_number VARCHAR(20), \
                    Start_call INT(11), \
                    End_call INT(11), \
                    Cost INT(20), \
                    PRIMARY KEY (Call_Id));"
            )
        logging.info("Checking table")
