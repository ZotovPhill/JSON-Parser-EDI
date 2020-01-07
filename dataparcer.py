import json
import os
import glob
import re
import logging
from myconfig import MyConfiguration

"""
Module for parse data from json file and transmit records to
next module. Also making checks for positive format data
(Null fields and regex pattern matching).
"""


class DataParcer:
    def __init__(self, file_path):
        self.file_path = file_path
        """
        Phone number pattern include simple Russian and Belarusian
        (example: +7(077)123-4567, +375(25)123-45-67);
        Digits limit of 10 characters for timestamps;
        Connection type for 3 type of connections.
        """
        self.rx_dict = {
            "number": re.compile(
                r"\+375\(\w{2}\)\w{3}-\w{2}-\w{2}|\+7\(\w{3}\)\w{3}-\w{4}"
            ),
            "digit": re.compile(r"\d{10}"),
            "type": re.compile(r"\\CDMA|GSM|LTE"),
        }
        self.mc = MyConfiguration.get_config("config.ini")

    def extract_file(self):
        """
        Take file from directiries and subdirectories, using glob as
        pattern matching for .json files. As file will be precessed and
        all good records inserted to database return control to delete a file.
        """
        for json_file in glob.glob(self.file_path + "**/*.json", recursive=True):
            yield json_file
            os.remove(json_file)
            logging.warning(f"File {json_file} was removed!")
        else:
            print("No file in directory")
            logging.warning("No file in directory")

    def extract_data(self):
        """
        Parse file, devides file on separate records because of json file
        structure. Takes each record and hands it for None values and
        regex checks. For Truthly result transmit record to main loop for
        inserting data to database. For negative result of check move record
        at bad format file processing.
        """
        for json_file in self.extract_file():
            with open(json_file) as json_data:
                json_obj = json.load(json_data)
                for json_item in json_obj:
                    if not self.check_data(json_item) and self.regex_check(json_item):
                        yield json_item
                    else:
                        logging.warning(f"Item was marked as bad format!")
                        self.move_bad_file(json_item)
                        continue

    def regex_check(self, json_item):
        """
        Match json record with pattern dictionary.
        """
        for item_key, item_value in json_item.items():
            for rx_key, rx_value in self.rx_dict.items():
                match = rx_value.search(str(item_value))
                if match:
                    break
            else:
                return False
        return True

    def check_data(self, json_item):
        """
        Take a dict of json item and check for None values
        in dict. all() will return True only when all the
        elements are Truthy(have values).
        """
        nones = not all(json_item.values())
        return nones

    def move_bad_file(self, json_item):
        """
        Move a record with item that cant pass regex pattern to
        a .txt file.
        """
        # Take a Path where stored a file for bad format records
        bad_file_path = self.mc["Path"]["bad_file"]
        with open(bad_file_path, mode="a") as badjson:
            badjson.write(f"{str(json_item)}\n")

    def print_values(self, data):
        print(dict(data))


if __name__ == "__main__":
    dp = DataParcer("S:\\FlaskTrain\\file\\")
    ef = dp.extract_file()
    ed = dp.extract_data()
    for i in ed:
        dp.print_values(i)
