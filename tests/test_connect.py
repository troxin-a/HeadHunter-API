from src.classes.connect import Connect


def test_connect():
    result = Connect().connect("https://api.hh.ru/vacancies")
    assert isinstance(result, list)
    assert len(result) > 0


def test_no_connect():
    result = Connect().connect("https://api.hh.ru")
    assert result == []
