from flask import Flask, request, render_template
import sqlite3

db = "bible-sqlite.db"
# con = sqlite3.connect(db)# connect to db
# cur = con.cursor()#create cursor to do ops

booklist = []
app = Flask(__name__)
# db connection
def db_conn():
    con = sqlite3.connect(db)# connect to db
    return con.cursor()
def get_bible_books():
    cur = db_conn()
    return cur.execute("SELECT * FROM key_english")
# get booklist
def get_booklist():
    for b in get_bible_books():
        booklist.append(b[1])
    return booklist
# get bookname using id
def bookname(id):
    # booklist = get_booklist()
    id = int(id)
    if id > len(booklist) or id<1:
        print(f'Type: {type(id)}')
        error = f'id {id} is out of range.'
        raise ValueError(error)
    else:
        return booklist[id-1]
#format bookname to bookid
def book_id(book_name):
    print(f'bookname: {book_name}')
    bk_code = booklist.index(book_name)
    bk_code +=1
    print(f'***bk_code: {bk_code} ; TYPE: {type(bk_code)} ***')
    if(int(bk_code) < 10):
        bk_code = f'0{bk_code}'
    # print(f'***bk_code2: {bk_code} ; TYPE2: {type(bk_code)} ***')
    return bk_code
# format chapter code to chapter
def chapter_id(chapter):
    if int(chapter)<10:
        return f'00{chapter}'
    if int(chapter)<100:
        return f'0{chapter}'
    else:
        return chapter
# keyword_search:
def keyword_search(kw_input):
    kw_result = []
    kresult = []
    version = 't_kjv'
    cmd = f'SELECT * FROM {version} WHERE T LIKE "%{kw_input}%" '
    cur = db_conn()
    kw_search = cur.execute(cmd)
    for k in kw_search.fetchall():
        k1 = bookname(k[1])
        # print(f'k1 is ... {k1}')
        kw_result.append(f'{k1} {k[2]}:{k[3]} {k[4]}')
    print(f'"{kw_input}" result count: {len(kw_result)}')
    for count, i in enumerate(kw_result):
        count +=1
        kresult.append(f'{count}.) {i}')
    if kresult != "":
        return kresult
    else: return 
# dropdown search:
def dropdown_search(id_input):
    if len(id_input) != 8:
        raise ValueError(f'"{id_input}" has incorrect length of {len(id_input)}')
    else:
        cur = db_conn()
        cmd = f'SELECT * from t_kjv where id = {id_input}'  
        result = cur.execute(cmd)
        id_rslt = result.fetchone()
        id_result = f'{bookname(id_rslt[1])} {id_rslt[2]}:{id_rslt[3]}: {id_rslt[4]}'
    return id_result

# search / index route
@app.route('/')
def search():
    print("Index page...")
    versecount = 160
    chaptercount = 150
    booklist = []
    booklist = get_booklist() # get booklist
    return render_template("index.html",books=booklist,versecount=versecount,chaptercount=chaptercount )

# results route
@app.route('/results', methods=['GET'])
def results():
    kw_result = []
    print("Results page...")
    # 1. kw search. TODO: wrap in func
    kw_input = request.args.get('kw')
    # kw_result = keyword_search(kw_input)
    searchtext = ''
    searchresult = ''
    id_input = ''
    id_result = ''
    kw_len = ''
    # 2. dropdown search
    bk_input = request.args.get('bk')
    ch_input = request.args.get('ch')
    vs_input = request.args.get('vs')
    # advanced id search
    id_input = request.args.get('id')

    if kw_input != '':
        kw_result = keyword_search(kw_input)
        kw_len = len(kw_result)
        print(f'Keyword Search result: {kw_input}; {kw_len}') 
    elif id_input != '':
        searchtext = id_input 
        searchresult = dropdown_search(id_input)
        print(f' "{id_input}" search result: {searchresult}')
    else:
        #default is dropdown search
        searchtext = f'{bk_input} {ch_input}:{vs_input}'
        print(f'searchtext: {searchtext}')
        bk_id = book_id(bk_input)
        ch_id = chapter_id(ch_input)
        vs_id = chapter_id(vs_input)
        searchtext_id = f'{bk_id}{ch_id}{vs_id}'
        print(f'convert {searchtext} to searchtext_id code: {searchtext_id}')
        searchresult = dropdown_search(searchtext_id)

    return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist, kw_input=kw_input, kw_result=kw_result, kw_len=kw_len, id_input=id_input, id_result=id_result)
    

    # db operations 
    # con = sqlite3.connect(db)# connect to db
    # cur = con.cursor()#create cursor to do ops
    # books_cmd = "SELECT * FROM key_english" #TODO: option to search for different version eg t_kjv
    # books = cur.execute(books_cmd)
    # booklist=[]
    # for b in books:
    #     booklist.append(b[1])

    # # helper funcs within this func or can take them outside
    # def book_id(book_name):
    #     books = booklist
    #     bk_code = books.index(book_name)+1
    #     if(bk_code < 10):
    #         bk_code = f'0{bk_code}'
    #     return bk_code

    # def chapter_id(chapter):
    #     if len(chapter)<2:
    #         return f'00{chapter}'
    #     if len(chapter)<3:
    #         return f'0{chapter}'
    #     else:
    #         return chapter
    
    # # fetch bookname with bookid
    # def bookname(id):
    #     if id> len(booklist) or id<1:
    #         error = f'id {id} is out of range.'
    #         raise ValueError(error)
    #     else:
    #         return booklist[id-1]
    # # 1. kw search. TODO: wrap in func
    # kw_input = request.args.get('kw')
    # kw_result = []
    # if len(kw_input)>0:
    #     print(f'Keyword search: "{kw_input}"')
    #     version = 't_kjv'
    #     cmd = f'SELECT * FROM {version} WHERE T LIKE "%{kw_input}%" '
    #     kw_search = cur.execute(cmd)
    #     if kw_search != None:
    #         for count, res in enumerate(kw_search):
    #             count+=1 # Increment to start from 1
    #             kw_search.append(f'{count}). {bookname(res[1])} {res[2]}:{res[3]} {res[4]}')
    #         for r in kw_result:
    #             print(r)
    # kw_res_len = len(kw_result)
    # print(kw_res_len)

    # # 2. dropdown search
    # bk_input = request.args.get('bk')
    # ch_input = request.args.get('ch')
    # vs_input = request.args.get('vs')
    # id_input = request.args.get('id')

    # searchtext = f'{bk_input} {ch_input}:{vs_input}'
    # print(f'searchtext: {searchtext}')
    # bk_id = book_id(bk_input)
    # ch_id = chapter_id(ch_input)
    # vs_id = chapter_id(vs_input)
    # searchtext_id = f'{bk_id}{ch_id}{vs_id}'
    # print(f'convert {searchtext} to searchtext_id code: {searchtext_id}')
    # searchresult=''
    # id_result = ''
                
    # # execute SQL if kw_input is present search that instead of bcv
    # if len(kw_input) !=0 or kw_input != " ":
    #     # cmd = f'SELECT * from t_kjv where T LIKE "%{kw_input}%"'
    #     # results = cur.execute(cmd)
    #     count = 0
    #     count = count+1
    #     print(results.fetchall())
    #     if results.fetchone() != None:
    #         res = results.fetchone()
    #         print(f'one result: {res}')
    #         kw_result.append(res)
    #         # kw_result.append(f'{count}). {booklist[res[1]]} {res[2]}:{res[3]} {res[4]}')  
    #     if (results.fetchmany(2) !=None):
    #         res = results.fetchall()
    #         for r in res:
    #             kw_result.append(f'{count}). {booklist[r[1]]} {r[2]}:{r[3]} {r[4]}')
    #             count+=1
        
            

    #     # for count, res in enumerate(results):
    #     #     if res:
    #     #         print(f'result: {res}; [#{count}]')
    #     #         count = count+1
    #     #         kw_result.append(f'{count}). {booklist[res[1]]} {res[2]}:{res[3]} {res[4]}')
    #     #         print(f'Item {count}: {booklist[res[1]]} {res[2]}:{res[3]} {res[4]}')
    #     #     # else:

    # else:
    #     print(f'no keyword to be searched.')

    # if len(searchtext_id) > 1:
    #     cmd = f'SELECT * from t_kjv where id = {searchtext_id}'  
    #     results = cur.execute(cmd)
    #     rslt = results.fetchone()
    #     searchresult = f'{searchtext}: {rslt[4]}'

    # if len(id_input)==8:
    #     cmd = f'SELECT * from t_kjv where id = {id_input}'  
    #     resul = cur.execute(cmd)
    #     id_rslt = resul.fetchone()
    #     id_result = f'{id_input}: {id_rslt[4]}'

    # # kw_result)
    # kw_len = len(kw_result)
    # print(f'Keyword Search result: {kw_result}; {kw_len}') 
    # print(f'Dropdown Search result: {searchresult}') 
    # print(f'ID Search result: {id_result}') 

    # con.close()
    # return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist, kw_input=kw_input, kw_result=kw_result, kw_len=kw_len, id_input=id_input, id_result=id_result)
    # return render_template("results.html")
