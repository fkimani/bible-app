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
    for a in versions:
        if vsn in a[1]:
            abbrev = a[2]
    return abbrev
# KEYWORD search: vsn default set in frontend (t_kjv)
def keyword_search(kw_input,bk_version):
    kw_result = []
    kresult = []
    cmd = f'SELECT * FROM {bk_version} WHERE T LIKE "% {kw_input}%" '
    cur = db_conn()
    kw_search = cur.execute(cmd)
    for k in kw_search.fetchall():
        k1 = bookname(k[1])
        kw_result.append(f'{k1} {k[2]}:{k[3]} {k[4]}')
    print(f'keyword "{kw_input}" mentioned {len(kw_result)} times.')
    for count, i in enumerate(kw_result):
        count +=1
        kresult.append(f'{count}.) {i}')
    if kresult != "":
        return kresult
    else: return 
# DROPDOWN search:
def dropdown_search(id_input, bk_version):
    if len(id_input) != 8:
        raise ValueError(f'"{id_input}" has incorrect length of {len(id_input)}')
    else:
        print(f'Dropdown single verse search. {id_input}')
        cur = db_conn()
        cmd = f'SELECT * from {bk_version} where id = {id_input}'  
        result = cur.execute(cmd)
        id_rslt = result.fetchone()
        id_result = [] # try me delete me if fail
        id_result = f'{bookname(id_rslt[1])} {id_rslt[2]}:{id_rslt[3]}: {id_rslt[4]}'
    return id_result
# DROPDOWN search - verse range 
def dropdown_range_search(id_input1,id_input2,bk_version):
    cur = db_conn()
    if len(id_input1) != 8 or len(id_input2) != 8:
        raise ValueError(f'id has incorrect length.')
    else:
        print(f'Dropdown multi verse search. {id_input1} - {id_input2}')
        cmd = f'SELECT * from {bk_version} where id BETWEEN {id_input1} AND {id_input2} '  # vs range
        result = cur.execute(cmd)
        id_rslt = result.fetchall()
        id_result = []
        for idr in id_rslt:
            id_result.append(f'{bookname(idr[1])} {idr[2]}:{idr[3]}: {idr[4]}')
    return id_result
# convert code to bcv : 01001002 -> Gen 1:2
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
    print(f'get_bkcode searchtext: {searchtext}')
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
    print("Results page...")
    # TODO: can reduce the vars
    searchtext = ''
    searchresult = []
    id_input = ''
    id_result = ''
    kw_len = ''
    bcv = ''
    # TODO: if can abstract some of it in func or put vars in dict
    # results object vars
    kw_input = request.args.get('kw')
    bk_version = request.args.get('version')
    bk_version_nm = get_version_abbrev(bk_version)
    bk_input = request.args.get('bk')
    ch_input = request.args.get('ch')
    vs_input = request.args.get('vs')
    vs_end_input = request.args.get('vs_end')
    id_input = request.args.get('id')
    # format vars 
    bk_id = book_id(bk_input)
    ch_id = chapter_id(ch_input)
    vs_id = chapter_id(vs_input)
    vs_end_id = chapter_id(vs_end_input)
    # if dropdown vrs range
    if vs_end_input != '0':
        bcv = f'{bk_input} {ch_input}:{vs_input}-{vs_end_input}'
        print(f'Multi-verse search for: {bcv}')
    else:
        bcv = f'{bk_input} {ch_input}:{vs_input}'
        print(f'Single verse search for: {bcv}')
    # 1. kw search advanced (has no keyword)
    if len(kw_input) > 0:
        searchtext = kw_input
        bcv = searchtext
        print(f'Keyword search "{bcv}" ')
        searchresult = keyword_search(kw_input,bk_version)
        kw_len = len(searchresult)
    # 2. id search 
    elif len(id_input) > 0:
        kw_len = 0
        searchtext = id_input 
        bcv = get_bcv(searchtext)
        searchresult = dropdown_search(id_input,bk_version)
        print(f' "{id_input}" search result: {searchresult}')
    # 3.a dropdown single search (default)
    elif vs_end_input == '0': #dropdwn single search
        kw_len = 0
        searchtext = dict([('bk',bk_input), ('ch',ch_input), ('vs',vs_input)])
        print(f'Single searchtext in results page: {searchtext}')
        searchtext_id = f'{bk_id}{ch_id}{vs_id}'
        searchtext_id = get_bkcode(searchtext)
        bcv = get_bcv(searchtext_id)
        print(f'Convert {searchtext} to searchtext_id code: {searchtext_id}')
        searchresult = dropdown_search(searchtext_id,bk_version)
        searchresult = f'{searchresult}'
    elif vs_end_input != '0': # 3b. dropdown multi search
        kw_len = 0
        searchtext = dict([('bk',bk_input), ('ch',ch_input), ('vs',vs_input)])
        searchtext_id1 = f'{bk_id}{ch_id}{vs_id}' # can abstract this row
        searchtext_id2 = f'{bk_id}{ch_id}{vs_end_id}'
        print(f'Multi-verse searchtext in results page: {bcv}')
        searchresult = dropdown_range_search(searchtext_id1,searchtext_id2,bk_version)
        # for sr in searchresult:
        #     print(sr) 
    else:
        print("**nothing found nothing to do.")
        kw_len = 0
        bcv = "NONE"
        searchtext = "NONE"
        searchresult = ["nothing comes up in results."]
    print(f'Results are in: {searchresult}')
    print(f'Results type: {type(searchresult)}')

            # TODO: clean up return vars  -put in dict kw_input is searchtext so use searchtext
    return render_template("results.html", searchtext=searchtext, results=searchresult, booklist=booklist, kw_len=kw_len, id_input=id_input, id_result=id_result, bk_version=bk_version,bk_version_nm=bk_version_nm, bcv=bcv)
    
