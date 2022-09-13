from flask import Flask, request, render_template
import sqlite3

db = "bible-sqlite.db"

app = Flask(__name__)

@app.route('/')
def search():
    print("Index page")
    return render_template("index.html", results="this is it!")

@app.route('/results', methods=['GET'])
def results():
    print("results page")
    return


