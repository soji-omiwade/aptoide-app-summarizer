#!flask/bin/python
from flask import Flask, request, render_template, jsonify
from os import environ
import lib.scraper
import sys

app = Flask(__name__)


@app.route('/')
def index():
    print("foo", file=sys.stderr)
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    url = request.form['search']
    data = lib.scraper.extract_info(url)
    print(url, data, file=sys.stderr)
    if isinstance(data, list):
        keys = ['Feature', 'Value']
        return render_template('index.html', data=data, keys=keys)
    else:
        return render_template('index.html', invalid_data=data)

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
