from src.yt_scrapper import YtScrapper
import pytest

yscrap = YtScrapper('https://www.google.com/watch?v=eY1FF6SEggk',20,r"/Users/lindaoranya/downloads/chromedriver")

def test_video_url_match():
    with pytest.raises(AttributeError) as error:
        yscrap.match_youtube_url()
    assert str(error.value) == "Expected a Youtube url"


def test_input():
    with pytest.raises(ValueError) as err:
        yscrap.checkinput("20",int)
    assert str(err.value) == "Expected <class 'int'> instead of 20"


def test_link_response_code():
    with pytest.raises(OSError) as oserr:
        yscrap.check_video_url()
    assert str(oserr.value) == "Invalid response"