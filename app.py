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
    versecount = 160
    chaptercount = 150
    return render_template("index.html", books=booklist, versecount=versecount,chaptercount=chaptercount )

@app.route('/results', methods=['GET'])
def results():
    print("Results page...")

    # db operations 
    con = sqlite3.connect(db)# connect to db
    cur = con.cursor()#create cursor to do ops
    books_cmd = "SELECT * FROM key_english" #fetch books 
    books = cur.execute(books_cmd)
    booklist=[]
    for b in books:
        booklist.append(b[1])
        # booklist.append(b)
    # print(f'books:\n ')
    # for bl in booklist:
    #     print(bl)

    # UTLITIES: helper funcs within this func or can take them outside
    def book_id(book_name):
        books = booklist
        bk_code = books.index(book_name)+1
        print(f'print bk_code: {bk_code}')
        print(f'print bk_code type: {type(bk_code)}')
        if(bk_code < 10):
            bk_code = f'0{bk_code}'
        return bk_code

    def chapter_id(chapter):
        print(f'{chapter} type: {type(chapter)}; LEN: {len(chapter)}')
        if len(chapter)<2:
            print(f'fetch chapter/vs code when <10: {chapter}')
            return f'00{chapter}'
        if len(chapter)<3:
            print(f'fetch chapter/vs code when <100: {chapter}')
            return f'0{chapter}'
        else:
            print(f'fetch chapter/vs code (>100 no change): {chapter}')
            return chapter

    # searchtext = request.args.get('id')
    bk_input = request.args.get('bk')
    ch_input = request.args.get('ch')
    vs_input = request.args.get('vs')

    searchtext = f'{bk_input} {ch_input}:{vs_input}'
    print(f'Searching for {searchtext}')
    bk_id = book_id(bk_input)
    ch_id = chapter_id(ch_input)
    vs_id = chapter_id(vs_input)
    searchtext_id = f'{bk_id}{ch_id}{vs_id}'
    print(f'searchtext_id ID: {searchtext_id}')
    # execute SQL
    cmd = f'SELECT * from t_kjv where id = {searchtext_id}'#search statement
    cur.execute(cmd)# execute statement
    # purse results
    results = cur.fetchone()
    for _ in results:
        # bk = results[1]
        # ch = results[2]
        # vs = results[3]
        text = results[4]
        # print(row)
    # bk = bk-1# array starts from zero 
    # bookname = booklist[bk][1] #(1, 'Genesis', 'OT', 1)
    # bookname = booklist[bk][1] #(1, 'Genesis', 'OT', 1)
    # print(f'{bk} book name: {bookname}')
    # searchresult = f'{bookname}:{ch}:{vs}: {text}'
    searchresult = f'{searchtext}: {text}'
    print(f'Search result: {searchresult}') 

    # con.close()
    return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist)
    


