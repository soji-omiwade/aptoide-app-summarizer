# aptoide-app-summarizer

Flask App to scrape and and extract app information from aptoide


Problem Statement:
After submitting the [aptoide app] URL, the website returns a page displaying
the following information about the App:
App's name
App's version
Number of downloads
Release date
App's description

To solve this problem, this script uses the BeautifulSoup API to parse the
aptoide html content. Of course, the parsing can be done with little or no use
of the BeautifulSoup module. For extensibility though, I used APIs when
possible. The idea is that we shouldn't reinvent the wheel by doing
what an established library has succeeded in doing. This makes my code
much less in content, and hence less confusing, and hence extensible.

If the content of the site changes and hence breaks this script, then we
may just need to change how we call the BeautifulSoup APIs and a little bit of
this script too. This should be quick.

The script is highly functional and every function returns only one type. This
allows for easier debugging and test case development. See the following for
example: ./tests/test_scraper.py

Finally, corner and edge cases are handled, where the site content has changed
or the URL is not an aptoide app URL    



## Usage


Access via http://localhost:8080

### Python

```bash
python main.py
```

Access via http://localhost:8080

> Set environment variable `PORT` locally to change listening port from `8080`
### Stack
- Python 3
- BeautifulSoup4
- Jquery

