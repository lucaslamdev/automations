import os
import requests
import bs4
from flask import Flask, render_template, jsonify
import json
import sqlite3

app = Flask(__name__)
class Company:
    def __init__(self, name):
        self.name = name
        self.url = "https://{0}.gupy.io/".format(name)
        self.file_name = "vagance_{0}.json".format(name)

    def get_html_vagance(self):
        html_complete = requests.get(self.url).text
        html_parsed = bs4.BeautifulSoup(html_complete, "html.parser")
        vagance_table = str(html_parsed.find_all("div", class_="job-list"))
        vagance_table = self.remove_html_trash(vagance_table)
        return vagance_table

    def remove_html_trash(self, vagance_table):
        vagance_table = vagance_table.replace("[", "")
        vagance_table = vagance_table.replace("]", "")
        vagance_table = vagance_table.replace("/job/", "{0}/job/".format(self.url))
        return vagance_table

    def save_vagance(self, data_vagance_table):
        with open("vagance_{0}.json".format(self.name), "w") as vagance_file:
            json.dump(data_vagance_table, vagance_file)

    def check_file_exist(self):
        return bool(os.path.isfile("{0}.json".format(self.file_name)))

    def diff_verify(self):
        pass

def get_company_list():
    conn = sqlite3.connect("vagance.db")
    c = conn.cursor()
    c.execute("SELECT name FROM vagance")
    company_list_trash = c.fetchall()
    company_list = []
    for company in company_list_trash:
        company = str(company)
        company = company.replace("(", "")
        company = company.replace(")", "")
        company = company.replace("'", "")
        company = company.replace(",", "")
        company_list.append(company)
    conn.close()
    return company_list
    
@app.route("/")
def gupy_vagance():
    list_companies = [Company("compass"), Company("ilegra")]
    return render_template(
        "index.html",
        list_companies=list_companies,
    )

@app.route("/gupy/<company_name>")
def gupy_one_vagance(company_name):
    company = Company(company_name)
    list_companies = [company]
    return render_template(
        "index.html",
        list_companies=list_companies,
    )

@app.route("/add/<company_name>")
def add_company(company_name):
    conn = sqlite3.connect("company.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS company (name text)")
    c.execute("SELECT name FROM company WHERE name=?", (company_name,))
    if c.fetchone() is None:
        c.execute("INSERT INTO company VALUES (?)", (company_name,))
        conn.commit()
        conn.close()
        return "Company {0} added".format(company_name)
    conn.close()

@app.route("/remove/<company_name>")
def remove_company(company_name):
    conn = sqlite3.connect("company.db")
    c = conn.cursor()
    c.execute("DELETE FROM company WHERE name=?", (company_name,))
    conn.commit()
    conn.close()
    return "Company {0} removed".format(company_name)

@app.route("/gupy_list_json/")
def gupy_list():
    conn = sqlite3.connect("company.db")
    c = conn.cursor()
    c.execute("SELECT name FROM company")
    company_list = c.fetchall()
    conn.close()
    return jsonify(company_list)

@app.route("/gupy_list/")
def gupy_list_html():
    company_list = get_company_list()
    list_companies = []
    for company in company_list:
        list_companies.append(Company(company))
    return render_template(
        "index.html",
        list_companies=list_companies,
    )

# heroku
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# local
# app.run(host="0.0.0.0", port=5000)
