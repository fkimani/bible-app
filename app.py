from flask import Flask, request, render_template
import sqlite3

db = "bible-sqlite.db"

app = Flask(__name__)

@app.route('/')
def search():
    print("Index page...")
    return render_template("index.html")

@app.route('/results', methods=['GET', 'POST'])
def results():
    print("Results page...")
    searchtext = request.args.get('id')
    print(f'searchtext: {searchtext}')
    # db operations here with searchtext
    return render_template("results.html", results=searchtext)


