import configparser
from os import path

from config import ROOT_DIR


def get_settings():
    """
    Читает настройки подключения к базе данных из ini-файла
    """
    config = configparser.ConfigParser()
    path_settings = path.join(ROOT_DIR, "settings.ini")
    config.read(path_settings)

    if not config.has_section("Database"):
        print("No section Database")
        exit()
    if not config.has_option("Database", "host"):
        print("No option host")
        exit()
    if not config.has_option("Database", "dbname"):
        print("No option dbname")
        exit()
    if not config.has_option("Database", "port"):
        print("No option port")
        exit()
    if not config.has_option("Database", "user"):
        print("No option user")
        exit()
    if not config.has_option("Database", "password"):
        print("No option password")
        exit()
    if not config["Database"]["dbname"]:
        print("Not set dbname")
        exit()

    if not config.has_section("CompanyID"):
        print("No section CompanyID")
        exit()

    list_id = config["CompanyID"]["list_id"].split(" ")

    return {item[0]: item[1] for item in config.items("Database")}, list_id
