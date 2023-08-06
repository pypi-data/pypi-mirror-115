import re
import ast

import functools as ft

from bs4 import BeautifulSoup

from mangakatana import siterequests


class Chapter:
    def __init__(self, soup):
        self._soup = soup

    @ft.cached_property
    def title(self): return self._soup.find("a").text

    @ft.cached_property
    def url(self): return self._soup.find("a").get("href")

    @ft.cached_property
    def chapter(self): return ast.literal_eval(re.search("[\d\.\d]+", self.title).group())


class ChapterList:
    def __init__(self, url):
        self.url = url

    @ft.lru_cache()
    def get(self):
        page_soup = BeautifulSoup(siterequests.get(self.url).content, "html.parser")

        return [Chapter(tr) for tr in page_soup.find_all("tr")][::-1]
