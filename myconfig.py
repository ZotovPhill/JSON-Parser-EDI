from configparser import ConfigParser
import os


class MyConfiguration:
    def get_config(config_file):
        """
        Method create an interface to access and reading
        information from config file. Rerurn ConfigParser object.
        For recieving value from config file call object method with
        reference to sections and keys with values.
        Config file always storing values internally as strings
        """
        config = ConfigParser()
        found = config.read(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), config_file)
        )
        if not found:
            raise ValueError("No config file found!")
        return config


if __name__ == "__main__":
    mc = MyConfiguration()
    MyConfiguration.get_config("conig.ini")
