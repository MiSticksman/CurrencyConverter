import os

import requests, jsonify
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from forms import ContactForm
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

LINK_URL = 'http://www.cbr.ru/scripts/XML_daily.asp'

quotes = requests.get(LINK_URL)
with open('static/encoding.xml', 'wb') as local_file:
    local_file.write(quotes.content)

infile = open("static/encoding.xml", "rb")
contents = infile.read()
soup = BeautifulSoup(contents, 'xml')


class Data:
    def __init__(self):
        self.char_codes = soup.find_all('CharCode')
        self.names = soup.find_all('Name')
        self.values = soup.find_all('Value')
        self.nominals = soup.find_all("Nominal")
        self.map_valute = {}
        self.map_nominal = {}
        for char, value in zip(self.char_codes, self.values):
            self.map_valute[char.get_text()] = float(value.get_text().replace(',', '.'))
        for char, nominal in zip(self.char_codes, self.nominals):
            self.map_nominal[char.get_text()] = int(nominal.get_text())
        self.in_rubles = []
        for value, nominal in zip(self.values, self.nominals):
            self.in_rubles.append(float("{0:.3f}".format(float(value.get_text().replace(',', '.')) / float(nominal.get_text()))))
        self.size = len(self.values)
        self.input_res = 5
        self.output_res = 0
@app.route('/')
def index():
    data = Data()
    return render_template('index.html', data=data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    data = Data()
    form = ContactForm()
    name_in = None
    name_out = None
    if request.method == 'POST':
        data.input_res = float(request.form['value_input'])
        name_in = request.form['input_name']
        name_out = request.form['output_name']
        data.output_res = float("{0:.3f}".format(float(data.map_valute[name_in] / data.map_nominal[name_in]) / (data.map_valute[name_out] / data.map_nominal[name_out]) * data.input_res))
    return render_template('converter.html', data=data, form=form, name_in=name_in, name_out=name_out)


if __name__ == "__main__":
    app.run(debug=True)

