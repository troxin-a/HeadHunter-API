from pytest import fixture

from src.classes.connect import Connect


@fixture
def class_connect():
    return Connect("https://api.hh.ru")
