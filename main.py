#!flask/bin/python
from flask import Flask, request, render_template
from os import environ
import scraper
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    url = request.form['search']
    data, error = scraper.get_app_summary(url)
    if not error:
        keys = ['Feature', 'Value']
        return render_template('index.html', data=data, keys=keys)
    else:
        return render_template('index.html', invalid_data=error)


@app.errorhandler(404)
def page_not_found(e):
    code = '404'
    return render_template('error.html', code=code), 404


@app.errorhandler(500)
def internal_server_error(e):
    code = '500'
    return render_template('error.html', code=code), 500


@app.errorhandler(503)
def service_unavailable(e):
    code = '503'
    return render_template('error.html', code=code), 503


if __name__ == '__main__':
    PORT = environ.get('PORT') or 8080
    if sys.version_info[0] < 3 and sys.version_info[1] < 2:
        print('Requires minimum Python 3.2')
        quit()
    app.run(host='0.0.0.0', port=PORT)
