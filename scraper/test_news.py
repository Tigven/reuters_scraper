import datetime
import pytest
import pytz

from news import News


def test_parse_full_text():
    # TODO
    pass


def test_to_dict():
    sample = News("title", "description", "published", "url", "full_text")
    assert sample.to_dict() == {
        "title": "title",
        "description": "description",
        "url": "url",
        "published": "published",
        "full_text": "full_text",
    }


def test_to_csv():
    sample = News("title", "description", "url", "published", "full_text")
    assert sample.to_csv() == '"title","description","url","published","full_text"'


def test_from_dict():
    from_dict = News.from_dict(
        {
            "title": "title",
            "description": "description",
            "url": "url",
            "published": "published",
            "full_text": "full_text",
        }
    )
    assert from_dict.title == "title"
    assert from_dict.description == "description"
    assert from_dict.url == "url"
    assert from_dict.published == "published"
    assert from_dict.full_text == "full_text"


def test_news_from_feed():
    test_feed = {
        "title": "American dies of coronavirus in China; five Britons infected in French Alps",
        "summary": 'A 60-year-old American has died of the new coronavirus, the first confirmed non-Chinese death of the illness, U.S. officials said, as millions of Chinese began returning home after a Lunar New Year break that was extended to try to contain the outbreak.<div class="feedflare">\n<a href="http://feeds.reuters.com/~ff/reuters/topNews?a=OmyoX_6P_ok:xVts69RBOpQ:yIl2AUoC8zA"><img src="http://feeds.feedburner.com/~ff/reuters/topNews?d=yIl2AUoC8zA" border="0"></img></a> <a href="http://feeds.reuters.com/~ff/reuters/topNews?a=OmyoX_6P_ok:xVts69RBOpQ:V_sGLiPBpWU"><img src="http://feeds.feedburner.com/~ff/reuters/topNews?i=OmyoX_6P_ok:xVts69RBOpQ:V_sGLiPBpWU" border="0"></img></a> <a href="http://feeds.reuters.com/~ff/reuters/topNews?a=OmyoX_6P_ok:xVts69RBOpQ:-BTjWOF_DHI"><img src="http://feeds.feedburner.com/~ff/reuters/topNews?i=OmyoX_6P_ok:xVts69RBOpQ:-BTjWOF_DHI" border="0"></img></a>\n</div><img src="http://feeds.feedburner.com/~r/reuters/topNews/~4/OmyoX_6P_ok" height="1" width="1" alt=""/>',
        "link": "http://feeds.reuters.com/~r/reuters/topNews/~3/OmyoX_6P_ok/american-dies-of-coronavirus-in-china-five-britons-infected-in-french-alps-idUSKBN20003J",
        "published": "Sat, 08 Feb 2020 12:22:37 -0500",
    }

    item_from_feed = News.from_feed(test_feed)
    assert (
        item_from_feed.title
        == "American dies of coronavirus in China; five Britons infected in French Alps"
    )
    assert (
        item_from_feed.description
        == "A 60-year-old American has died of the new coronavirus, the first confirmed non-Chinese death of the illness, U.S. officials said, as millions of Chinese began returning home after a Lunar New Year break that was extended to try to contain the outbreak."
    )
    assert (
        item_from_feed.url
        == "http://feeds.reuters.com/~r/reuters/topNews/~3/OmyoX_6P_ok/american-dies-of-coronavirus-in-china-five-britons-infected-in-french-alps-idUSKBN20003J"
    )
    assert item_from_feed.published == datetime.datetime(
        2020, 2, 8, 17, 22, 37, tzinfo=pytz.utc
    )

