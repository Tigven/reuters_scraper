from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_time
import pytz
import re
import requests


class News:
    def __init__(self, title, description, published, url, full_text=None):
        self.title = title
        self.description = description
        self.published = published
        self.url = url
        self.full_text = full_text

    
    @classmethod
    def from_feed(cls, feed_item: dict):
        """
        Make New object from feed item dict
        """
        title = feed_item.get('title')

        description = feed_item.get('summary')
        # extract text of description
        description = re.search(r'^(.*?)<', description).group(1)

        text_pubdate = feed_item.get('published')
        parsed_pubdate = parse_time(text_pubdate)
        utc_pub_date = parsed_pubdate.astimezone(pytz.utc)

        url = feed_item.get('link')

        return cls(title, description, utc_pub_date, url)
    
    def set_text_from_html(self, html, article_class="StandardArticleBody_body"):
        """
        Parse full text of article and set full_text attribute
        """
        soup = BeautifulSoup(html, features="lxml")
        tags = soup.find("div", {"class": article_class}).find_all('p', {'class':None}, text=True)
        self.full_text = ' '.join([tag.text.strip() for tag in tags])

    def to_dict(self):
        """
        Serialize item to dict
        """
        return {
            'title': self.title,
            'description': self.description,
            'published': self.published,
            'url': self.url,
            'full_text': self.full_text
        }

    @classmethod
    def from_dict(cls, item_dict):
        """
        Create object from dict
        """
        return cls(**item_dict)

    def to_csv(self, delimeter=','):
        return '"{}"{}"{}"{}"{}"{}"{}"{}"{}"'.format(
            self.title, delimeter,
            self.description, delimeter,
            self.published, delimeter,
            self.url, delimeter,
            self.full_text)
