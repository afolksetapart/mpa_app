# TODO: add docstrings, add print statements

import csv
import os
from scraper.scribsearch import ScribSearch


if __name__ == "__main__":
    with open('titles.csv') as titles:
        title_reader = csv.DictReader(titles)
        title_list = list(title_reader)

        for title in title_list:
            s = ScribSearch.const_q(title)
            s.execute()
