import csv

import arbiter
from scraper.page import ResultPage
from scraper.title import Title

import urllib.parse


class ScribSearch():
    def __init__(self, current_row):
        self.current_row = current_row
        self.queries = []
        self.title = None

    @classmethod
    def const_q(cls, current_row):
        """Initialize ScribSearch with URL queries"""
        search = cls(current_row=current_row)
        search.title = Title.parse_record(search.current_row)

        url_name = urllib.parse.quote(search.title.title.lower())
        pg_num = 1

        while pg_num < 11:
            search.queries.append(
                (f'https://www.scribd.com/search?content_type'
                 '=documents&page={pg_num}&query={url_name}&language=1'))
            pg_num += 1

        return search

    def commit(self, rating, link):
        """Write valid result to CSV"""
        with open('reports.csv', 'a') as report:
            fieldnames = ['TITLE', 'FROM/COMPOSER',
                          'URL', 'CLAIM', 'RATING']
            writer = csv.DictWriter(report, fieldnames=fieldnames)
            if report.tell() == 0:
                writer.writeheader()
                writer.writerow(
                    {'TITLE': self.title.title,
                     'FROM/COMPOSER': self.title.from_comp,
                     'URL': f"\"{link}\"",
                     'CLAIM': self.title.claim,
                     'REVIEW': rating})

    def execute(self):
        """Load results and commit if result found"""
        for query in self.queries:
            rp = ResultPage.get_documents(query)
            rp.fetch_previews()

            for result in rp.results:
                candidate = arbiter.Candidate.evaluate(result.preview)
                arb = arbiter.Arbiter.compare(self.title, candidate)

                if arb.determine():
                    self.commit(arb.accuracy, result.doc_link)
                else:
                    continue
