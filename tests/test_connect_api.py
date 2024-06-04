def test_connect_api(api_obj):
    result = api_obj._connect("https://api.hh.ru/vacancies")
    assert isinstance(result, list)
    assert len(result) > 0


def test_no_connect_api(api_obj):
    result = api_obj._connect("https://api.hh.ru")
    assert isinstance(result, list)


def test_get_vacancies_data(api_obj):
    data = api_obj.get_vacancies_data("python", 3)
    assert len(data) == 3
    assert "python" in data[0]["name"].lower()
