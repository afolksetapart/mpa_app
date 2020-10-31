import csv

from helpers import header
from arbiter.arbiter import Arbiter
from arbiter.candidate import Candidate
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
                 f'=documents&page={pg_num}&query={url_name}&language=1'))
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
                    'URL': link,
                    'CLAIM': self.title.claim,
                    'RATING': rating})

    def execute(self):
        """Load results and commit if result found. 
        If 42 results (in a row) receive a score <= 1, the next title is considered."""
        ignored = 0

        for query in self.queries:
            if ignored < 42:
                ignored = 0
                header()
                print(f"searching for title '{self.title.title}'...\n")
                print(
                    f"scraping page {self.queries.index(query) + 1} for results...\n")
                rp = ResultPage.get_documents(query)
                print("scraping results for image preview urls...\n")
                rp.fetch_previews()

                print(
                    f"analyzing images on page {self.queries.index(query) + 1}...\n")
                for r in rp.results:
                    if r.preview == None:
                        ignored += 1
                        continue
                    else:
                        cand = Candidate.evaluate(r.preview)
                        arb = Arbiter.compare(self.title, cand)

                        if arb.determine():
                            print(
                                "match found...")
                            self.commit(arb.accuracy, r.doc_link)
                            if arb.accuracy == 1:
                                ignored += 1
                        else:
                            ignored += 1
                            continue
                print("\n")
            else:
                break
