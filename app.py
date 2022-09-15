from flask import Flask, request, render_template
import sqlite3

db = "bible-sqlite.db"

app = Flask(__name__)

@app.route('/')
def search():
    print("Index page...")
    con = sqlite3.connect(db)# connect to db
    cur = con.cursor()#create cursor to do ops
    books_cmd = "SELECT * FROM key_english" #fetch books 
    books = cur.execute(books_cmd)
    booklist=[]
    for b in books:
        booklist.append(b[1])
    print(f'Booklist count(expect 66): {len(booklist)}')#66 books expected
    return render_template("index.html", books=booklist)

@app.route('/results', methods=['GET', 'POST'])
def results():
    print("Results page...")
    searchtext = request.args.get('id')
    print(f'searchtext: {searchtext}')
    # db operations here with searchtext
    con = sqlite3.connect(db)# connect to db
    cur = con.cursor()#create cursor to do ops
    books_cmd = "SELECT * FROM key_english" #fetch books 
    books = cur.execute(books_cmd)
    booklist=[]
    for b in books:
        # booklist.append(b[1])
        booklist.append(b)
    # print(f'books:\n ')
    # for bl in booklist:
    #     print(bl)
    cmd = f'SELECT * from t_kjv where id = {searchtext}'#search statement
    cur.execute(cmd)# execute statement
    # purse results
    results = cur.fetchone()
    for _ in results:
        bk = results[1]
        ch = results[2]
        vs = results[3]
        text = results[4]
        # print(row)
    bk = bk-1# array starts from zero 
    bookname = booklist[bk][1] #(1, 'Genesis', 'OT', 1)
    # print(f'{bk} book name: {bookname}')
    searchresult = f'{bookname}:{ch}:{vs}: {text}'
    print(f'Search result: {searchresult}') 

    # con.close()
    return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist)
    


