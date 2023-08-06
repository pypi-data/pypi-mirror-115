#!/usr/bin/env python3
import json
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urlparse


class StopParsing(Exception): pass


class ImkinParser:
    allowed_domains = ["www.imdb.com", "www.kinopoisk.ru"]
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; WOW64; "
            "Trident/7.0; ASU2JS; rv:11.0) like Gecko"
        ),
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Language": "ru-RU"
    }
    
    def __init__(self, url, encoding="utf8", headers=None):
        if not self._validate_url(url):
            raise ValueError("only www.imdb.com and www.kinopoisk.ru are allowed")
        
        self._encoding = encoding
        
        if "kinopoisk" in url and "https" in url:
            self._url = url.replace("https", "http")
            self._parser = KinopoiskParser
        else:
            self._url = url
            self._parser = ImdbParser
        
        if headers is None:
            self._headers = self.default_headers
        else:
            self._headers = headers
    
    def _validate_url(self, url):
        if urlparse(url).netloc in self.allowed_domains:
            return True
        return False
    
    def _fetch(self):
        response = urlopen(Request(self._url, headers=self._headers))
        return response.read().decode(self._encoding, errors="ignore")
    
    def parse(self):
        parser = self._parser()
        html = self._fetch()
        try:
            parser.feed(html)
        except StopParsing:
            pass
        finally:
            parser.reset()
            parser.close()
        title, original, year, duration = parser.result
        if not title:
            parser = ImdbParser2()
            try:
                parser.feed(html)
            except StopParsing:
                pass
            finally:
                parser.reset()
                parser.close()
            title, original, year, duration = parser.result
        return title, original, year, duration


class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.original = ""
        self.year = ""
        self.duration = ""
    
    @property
    def result(self):
        return self.title, self.original, self.year, self.duration


class ImdbParser(ResultParser):
    def __init__(self):
        super().__init__()
        self._div_TitleBlock = False
        self._h1_TitleHeader = False
        self._div_OriginalTitle = False
        self._ul = False
        self._li = False
        self._a = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for n, v in attrs:
                if n == "class" and "TitleBlock" in v:
                    self._div_TitleBlock = True
                    return
                if n == "class" and "OriginalTitle" in v and \
                   self._div_TitleBlock:
                    self._div_OriginalTitle = True
        elif tag == "h1" and self._div_TitleBlock:
            for n, v in attrs:
                if n == "class" and "TitleHeader" in v:
                    self._h1_TitleHeader = True
        elif tag == "ul" and self._div_TitleBlock:
            self._ul = True
        elif tag == "li" and self._ul:
            self._li = True
        elif tag == "a" and self._li:
            self._a = True
    
    def handle_data(self, data):
        if self._h1_TitleHeader:
            self.title = data.strip()
            self._h1_TitleHeader = False
        elif self._div_OriginalTitle:
            self.original = data.split(":")[-1].strip()
            self._div_OriginalTitle = False
        elif self._li:
            if self._a and not self.year:
                self.year = data.strip()
                self._a = False
            elif "min" in data:
                duration = data.split()
                hours = [i for i in duration[0] if i.isdigit()]
                minutes = [i for i in duration[1] if i.isdigit()]
                duration = (int("".join(hours)) * 60) + int("".join(minutes))
                self.duration = str(duration)
                self._div_TitleBlock = False
    
    def handle_endtag(self, tag):
        if tag == "li" and self._ul:
            self._li = False
        if tag == "ul" and self._ul:
            raise StopParsing()


class ImdbParser2(ResultParser):
    def __init__(self):
        super().__init__()
        self._div_title = False
        self._h1 = False
        self._div_originalTitle = False
        self._span_titleYear = False
        self._a = False
        self._time = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for n, v in attrs:
                if n == "class" and "title_wrapper" in v:
                    self._div_title = True
                    return
                if n == "class" and "originalTitle" in v and self._div_title:
                    self._div_originalTitle = True
        elif tag == "h1" and self._div_title:
            self._h1 = True
        elif tag == "span" and self._h1:
            for n, v in attrs:
                if n == "id" and "titleYear" in v:
                    self._span_titleYear = True
        elif tag == "a" and self._span_titleYear:
            self._a = True
        elif tag == "time":
            for n, v in attrs:
                if n == "datetime" and "PT" in v:
                    self.duration = "".join([i for i in v if i.isdigit()])
            self._time = True
    
    def handle_data(self, data):
        if self._h1 and self._div_title and not self.title:
            self.title = data.strip()
        elif self._div_originalTitle and not self.original:
            self.original = data.strip()
        elif self._a and not self.year:
            self.year = data.strip()
            self._span_titleYear = False
            self._h1 = False
    
    def handle_endtag(self, tag):
        if tag == "time":
            raise StopParsing()


class KinopoiskParser(ResultParser):
    def __init__(self):
        super().__init__()
        self._script = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            for n, v in attrs:
                if n == "type" and v == "application/ld+json":
                    self._script = True
        elif tag == "iframe":
            raise StopParsing()
    
    def handle_data(self, data):
        if self._script:
            j = json.loads(data)
            self.title = j["name"]
            original = j.get("alternateName", "")
            if original:
                self.original = j["alternateName"]
            self.year = j["datePublished"]
            self.duration = j["timeRequired"]
            self._script = False
