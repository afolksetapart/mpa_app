import json
import re
import requests
import urllib.parse

from bs4 import BeautifulSoup


class ResultPage():
    def __init__(self):
        self.doc_links = []
        self.previews = []

    @staticmethod
    def get_scripts(url):
        """Requests URL and returns all script tags"""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all('script')

    @classmethod
    def get_documents(cls, url):
        """Scrape for individual document links"""
        scripts = get_scripts(url)
        json_script = str(scripts[-4])
        json_re = re.search(
            r'{"documents":{"content":{"documents":(.*)}}}}', json_script)
        json_raw = json_re.group(0).strip()
        processed_json = json.loads(json_raw)
        doc_list = processed_json['documents']['content']['documents']

        doc_links = []
        for doc in doc_list:
            doc_links.append(doc['reader_url'])

        page = cls(doc_links=doc_links)

    def fetch_previews(self):
        """Scrape doc_links for preview image links"""
        for doc in self.doc_links:
            scripts = get_scripts(doc)
            json_script = str(scripts[-6])
            json_re = re.search(
                r'"thumbnail_url":(.*),"title":', json_script)
            if json_re != None:
                img_url = json_re.group(1)[1:-1]
                self.previews.append(img_url)
            else:
                continue
