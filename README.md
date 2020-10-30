# Sheet Scraper
### A Web-Scraping Copyright Infringement App Built for the Music Publishers Association

Sheet Scraper is a web-scraping CLI that takes a CSV of sheet music titles (provided by the Music Publishers Association) and scrapes the popular document upload site Scribd for illegal postings of copyrighted work. 

## How It Works

Upon parsing each row in the MPA CSV for keywords and constructing a list of URLs, Sheet Scraper executes a search on Scribd for each title and scrapes image previews from the results. 

Each image preview is sent to the Google Vision API, which returns a list of labels (sheet music, etc.) as well as all the text it can read from the image. If the image is in fact sheet music (or tabs), Sheet Scraper will compile the text returned from Vision and execute a series of keyword searches, adding "points" to each document. 

If the document scores highly enough, the program will write all data from the original row related to each title (along with a URL for the infringing upload) to a new CSV, one row for each infringement.

## To Run

*(This project requires you to have pipenv installed)*

Install all project dependencies by navigating to the route directory and running:
```
pipenv install
```


*(This project requires GOOGLE_APPLICATION_CREDENTIALS)*

Learn more [here](https://cloud.google.com/vision).

Run **app.py** from the root directory with:
```
$ python3 app.py
```

## Built With

- Python
- BeautifulSoup
- Google Cloud Vision API
