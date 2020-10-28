import json
import re
import requests
import urllib.parse

from bs4 import BeautifulSoup


class ResultPage():
    doc_links = []

    @classmethod
    def get_documents(cls, url):
        """Scrape for individual document links"""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        scripts = soup.find_all('script')
        json_script = str(scripts[-4])
        json_raw = re.search(
            r'{"documents":{"content":{"documents":(.*)}}}}', json_script).group(0).strip()
        # json_raw = json_raw.group(0).strip()
        processed_json = json.loads(json_raw)
        doc_list = processed_json['documents']['content']['documents']

        doc_links = []
        for doc in doc_list:
            doc_links.append(doc['reader_url'])

        cls.create(doc_links=doc_links)
