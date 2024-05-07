from src.connect_api import ConnectAPI


def test_connect_api():
    result = ConnectAPI().connect("https://api.hh.ru/vacancies")
    assert isinstance(result, list)
    assert len(result) > 0


def test_no_connect_api():
    result = ConnectAPI().connect("https://api.hh.ru")
    assert result == []
