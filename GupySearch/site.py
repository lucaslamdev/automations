import requests
import bs4
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

def get_vagas(url):
    html_complete = requests.get(url).text
    html_parsed = bs4.BeautifulSoup(html_complete, 'html.parser')
    vagas = str(html_parsed.find_all('div', class_="job-list"))
    vagas = vagas.replace('[', '')
    vagas = vagas.replace(']', '')
    vagas = vagas.replace('/job/', '{0}/job/'.format(url))
    return vagas

@app.route('/')
def gupy():
    div_vagas = '''
    <html>
    <head>
    <title>Gupy</title>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" type="text/css" href="https://compass.gupy.io/statics/assets/css/career.css">
    </head>
    <body>
    <h1>Compasso</h1>
    {0}
    </hr>
    <h1>Ilegra</h1>
    {1}
    </body>
    </html>
    '''.format(get_vagas('https://compass.gupy.io/'), get_vagas('https://ilegra.gupy.io/'))
    return div_vagas


app.run(debug=True, host='0.0.0.0')
