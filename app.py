from flask import Flask, request, template_rendered
import sqlite3

db = "bible-sqlite.db"

app = Flask(__name__)

@app.route('/')
def search():
    print("hello world")

    return

@app.route('/results', methods=['GET', 'POST'])
def results():

    print("results")

    return


