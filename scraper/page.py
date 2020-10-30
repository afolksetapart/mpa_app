import json
import re
import requests
import urllib.parse

from scraper.result import Result

from bs4 import BeautifulSoup


class ResultPage():
    def __init__(self):
        self.results = []

    @staticmethod
    def get_scripts(url):
        """Requests URL and returns all script tags"""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all('script')

    @classmethod
    def get_documents(cls, url):
        """Scrape for individual document links"""
        page = cls()
        scripts = page.get_scripts(url)
        json_script = str(scripts[-4])
        json_re = re.search(
            r'{"documents":{"content":{"documents":(.*)}}}}', json_script)
        json_raw = json_re.group(0).strip()
        try:
            processed_json = json.loads(json_raw)
            doc_list = processed_json['documents']['content']['documents']
            for doc in doc_list:
                page.results.append(Result(doc_link=doc['reader_url']))
        except json.JSONDecodeError:
            pass

        return page

    def fetch_previews(self):
        """Scrape doc_links for preview image links"""
        for result in self.results:
            scripts = self.get_scripts(result.doc_link)
            json_script = str(scripts[-6])
            json_re = re.search(
                r"\"thumbnail_url\":\"(.[^\"]*)", json_script)
            if json_re != None:
                img_url = json_re.group(1)
                result.preview = img_url
            else:
                continue
