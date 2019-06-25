import pytest, sys, warnings, json, os
from io import StringIO
sys.path.insert(0, os.path.join(sys.path[0], ".."))
import weather

def test_getURL():
    assert weather.get_URL("123", "abc", "123") != "" or None
    
    url = weather.get_URL("123", "abc", "123")
    for e in ["123", "abc", "123"]:
        assert e in url

    assert type(weather.get_URL("123", "abc", "123")) == type(str())

def test_search():
    assert weather.search("Berlin") != [] or None
    assert type(weather.search("Berlin")) == type(list())

def test_getData():
    # Sample query from https://openweathermap.org/current
    url = "https://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b6907d289e10d714a6e88b30761fae22"
    assert weather.get_Data(url) != {} or None
    assert type(weather.get_Data(url)) == type(dict())