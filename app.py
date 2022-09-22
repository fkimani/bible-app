from flask import Flask, request, render_template
import sqlite3

db = "bible-sqlite.db"
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
        error = f'id {id} is out of range.'
        raise ValueError(error)
    else:
        return booklist[id-1]
#format bookname to bookid
def book_id(book_name):
    bk_code = booklist.index(book_name)
    bk_code +=1 # since array starts from 0
    bk_code = f'{bk_code}'
    return bk_code.zfill(2) #prepend zeros to have 2 digits
# format chapter code to chapter
def chapter_id(chvs):
    chvs = f'{chvs}'
    return chvs.zfill(3) #prepend zeros to have 3 digits
# get versions
def get_versions():
    cur = db_conn()
    vers = []
    vsns = cur.execute("SELECT * FROM bible_version_key")
    for v in vsns:
         vers.append(v)
    return vers
# #get version abbev
def get_version_abbrev(vsn):
    abbrev = ''
    versions = get_versions()
    print(f'Fetching "{vsn}" abbrev...')
    for a in versions:
        if vsn in a[1]:
            print(f'Fetched. {a[1]} = {a[2]} ')
            abbrev = a[2]
    return abbrev
def keyword_search(kw_input,bk_version):
    kw_result = []
    kresult = []
    # version = 't_kjv' #default version for now
    cmd = f'SELECT * FROM {bk_version} WHERE T LIKE "%{kw_input}%" '
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
def dropdown_search(id_input, bk_version):
    if len(id_input) != 8:
        raise ValueError(f'"{id_input}" has incorrect length of {len(id_input)}')
    else:
        cur = db_conn()
        cmd = f'SELECT * from {bk_version} where id = {id_input}'  
        result = cur.execute(cmd)
        id_rslt = result.fetchone()
        id_result = f'{bookname(id_rslt[1])} {id_rslt[2]}:{id_rslt[3]}: {id_rslt[4]}'
    return id_result
# convert code to bcv
def get_bcv(id_input):
    if len(id_input) != 8:
        raise ValueError(f'"{id_input}" has incorrect length of {len(id_input)}')
    bk_id = id_input[0:2]
    ch_id = id_input[2:5]
    vs_id = id_input[5:8]
    bk_name = bookname(bk_id)
    chapter = int(ch_id)
    verse = int(vs_id)
    bcv_format = f'{bk_name} {chapter}:{verse}'
    print(f'Decode {id_input} to bcv format: {bcv_format}')
    return bcv_format
# convert searchtext to 8 digit code
def get_bkcode(searchtext):
    # convert vars to searchable 8 digit ids
    r = f"{searchtext['bk']} {searchtext['ch']}:{searchtext['vs']}" 
    bid = book_id(searchtext['bk'])
    cid = chapter_id(searchtext['ch'])
    vid = chapter_id(searchtext['vs'])
    bcvid = f"{bid}{cid}{vid}" 
    print(f'Encode {r} to {bcvid}')
    return bcvid
# search / index route
@app.route('/')
def search():
    print("Index page...")
    versions = get_versions()
    # print(f'versions: {versions}')
    versecount = 160
    chaptercount = 150
    booklist = []
    booklist = get_booklist() # get booklist
    return render_template("index.html",books=booklist,versecount=versecount,chaptercount=chaptercount,versions=versions )

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
    bcv=''
    bk_version = request.args.get('version')
    bk_version_nm = get_version_abbrev(bk_version)
    # 2. dropdown search
    bk_input = request.args.get('bk')
    ch_input = request.args.get('ch')
    vs_input = request.args.get('vs')
    vs_end_input = request.args.get('vs_end')
    # advanced id search
    id_input = request.args.get('id')

    if kw_input != '':
        kw_result = keyword_search(kw_input,bk_version)
        kw_len = len(kw_result)
        print(f'Keyword Search result: {kw_input}; {kw_len}') 
    elif id_input != '':
        kw_len = 0
        searchtext = id_input 
        bcv = get_bcv(searchtext)
        searchresult = dropdown_search(id_input,bk_version)
        print(f' "{id_input}" search result: {searchresult}'
    else:
        #default is dropdown search
        kw_len = 0
        # TODO start changehere (=to func)
        # searchtext = f'{bk_input} {ch_input}:{vs_input}'
        searchtext = dict([('bk',bk_input), ('ch',ch_input), ('vs',vs_input)])
        # print(bcvid)
        # utilities.get_bkcode(bcvid)
        print(f'searchtext in results page: {searchtext}')
        bk_id = book_id(bk_input)
        ch_id = chapter_id(ch_input)
        vs_id = chapter_id(vs_input)
        vs_end_id = chapter_id(vs_end_input)
        # end changehere
        if vs_end_id != '':
            searchtext_id = f'{bk_id}{ch_id}{vs_id}'
            searchtext_id2 = f'{bk_id}{ch_id}{vs_end_id}'
            searchtext_id1 = get_bkcode(searchtext_id1)
            searchtext_id2 = get_bkcode(searchtext_id2)
            bcv1 = get_bcv(searchtext_id1)
            bcv2 = get_bcv(searchtext_id2)
            bcv = f'{bcv1}-{bcv2[5:7]}'
            print(f'bcv for vs-vs_end: {bcv}')
        else:
            searchtext_id = f'{bk_id}{ch_id}{vs_id}'
            searchtext_id = get_bkcode(searchtext)
            bcv = get_bcv(searchtext_id)
            print(f'convert {searchtext} to searchtext_id code: {searchtext_id}')
            searchresult = dropdown_search(searchtext_id,bk_version)

    return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist, kw_input=kw_input, kw_result=kw_result, kw_len=kw_len, id_input=id_input, id_result=id_result, bk_version=bk_version,bk_version_nm=bk_version_nm, bcv=bcv)
    
