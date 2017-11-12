# web-link-tester
[![Build Status](https://travis-ci.org/circa10a/web-link-tester.svg?branch=master)](https://travis-ci.org/circa10a/web-link-tester)
[![Docker Repository on Quay](https://quay.io/repository/circa10a/web-link-tester/status "Docker Repository on Quay")](https://quay.io/repository/circa10a/web-link-tester)
![Docker Automated buil](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)()
[![](https://images.microbadger.com/badges/image/circa10a/web-link-tester.svg)](https://microbadger.com/images/circa10a/web-link-tester "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/circa10a/web-link-tester.svg)](https://microbadger.com/images/circa10a/web-link-tester "Get your own version badge on microbadger.com")

Flask App to scrape and validate links via GUI or API

### [scrapeyour.site](http://scrapeyour.site)

## Usage

### Docker

```bash
docker run -d --name link-tester -p 80:80 circa10a/web-link-tester
```
### Python

```bash
python main.py 
```
**Note** This method may require to run as root unless you change the port number in `main.py`

Access via http://localhost

### API Usage

```bash
curl -X POST --data "https://www.github.com" http://localhost/api
```
### Stack
- Utilizes uwsgi/nginx for multiple workers/threading.
- Python 3
- BeautifulSoup4
- Jquery
