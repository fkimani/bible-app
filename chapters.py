from flask import Flask, request, render_template
import sqlite3
db = "bible-sqlite.db"
book = "Genesis"
# db connection
con = sqlite3.connect(db)
cur = con.cursor()

# deleteme there is now a functions for this
books_cmd = "SELECT * FROM key_english"
books = cur.execute(books_cmd)
booklist=[]
for b in books:
    # print(b)
    booklist.append(b[1])
# print(f'Booklist count(expect 66): {len(booklist)}')#66 books expected
# chapter_count = 0
# print(f'{book} has {chapter_count} chapters' ) 
# con.close()


# FUNCTIONS
# get bible books
def get_bible_books():
    return cur.execute("SELECT * FROM key_english")

# get booklist
def get_booklist():
    for b in get_bible_books():
        booklist.append(b[1])
    return booklist

# get tables
def get_tables():
    return cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

# get table count
def get_table_count():
    return cur.execute("SELECT count (*) FROM sqlite_master WHERE type='table' ;")

#schema
def get_schema():
    return cur.execute("SELECT sql FROM sqlite_master ;" )

# columns names
def get_column_names():
    return cur.execute("SELECT name FROM sqlite_master ;" )

#Get all versions
def get_versions():
    return cur.execute("SELECT * FROM bible_version_key")

# get one book       
def get_bible_book_one(bookid):
    return cur.execute(f'SELECT n FROM key_english WHERE b = {bookid}')

# search by id(complicated)
def search_id(someid):
    return cur.execute("SELECT * FROM t_kjv where id = '{}' ".format(someid) )
    
# keyword search
# def search_keyword(keyword):
#     if (keyword == 'not found'):
#         result = search_id('')
#     else:
#         result = cur.execute(f'SELECT * FROM t_kjv where T LIKE {keyword}') 
#     return result 
# tAKE 2
def search_keyword(keyword):
    if (len(keyword) < 1 ):
        return "ERROR: must provide keyword."
    else:
        print(f'Searching for "{keyword}"...')
        return printer(cur.execute(f'SELECT * FROM t_kjv  where t like "%{keyword}%" ') )
        # needs some work
        # return get_list(cur.execute(f'SELECT * FROM t_kjv  where t like "%{keyword}%" '))
        # for r in result:
        #     if r == None:
        #         print(f'{keyword} not found')
        #         return 
        #     print(r)
        #     print(f'{keyword} found')
        #     return result  
# get bookname:
def get_bookname(bookid):
    # book = booklist[bk][1]
    if bookid == 0 or bookid > 66:
        return "error: bad input. cannot be <0 or >66"
    return get_booklist()[bookid-1]

# print func results by iterating list
def printer(myfunc):
    for item in myfunc:
        print(item)
    
# iterate and add to list
def get_list(myfunc):
    l = []
    for item in myfunc:
        i = f'{get_bookname(item[1])}:{item[2]}:{item[3]}: {item[4]}'
        print(i)
        l.append(i)
    return 

# printer(get_table_count())
# printer(get_tables())
# printer(get_versions())
# bookid = '01'
# printer(get_bible_book_one(bookid))
# printer(get_bible_book_one('1'))

# try cmd in variables
book_info = "book_info"
bi = cur.execute(f'SELECT * FROM {book_info}' ) 
# printer(bi)
bible_version_key = "bible_version_key"
bvk = cur.execute(f'SELECT * FROM {bible_version_key}')
# printer(bvk)

# warning: cross reference is a lot of data -- LIMIT 50
# cross_reference = 'cross_reference'
# cr = cur.execute(f'SELECT * FROM {cross_reference} LIMIT 50' ) 
# printer(cr)

# key_abbreviations_english = "key_abbreviations_english"
# kae = cur.execute(f'SELECT * FROM {key_abbreviations_english}')
# printer(kae)

# genres of bible: law, history, prohpets, gospels, acts, eipstles, apocalyptic
# key_genre_english = "key_genre_english"
# kge = cur.execute(f'SELECT * FROM {key_genre_english}')
# printer(kge)

# Keys
# key_english = "key_english"
# ke = cur.execute(f'SELECT * FROM {key_english}')
# printer(ke)

# print(f'GET booklist: {get_booklist()}')


# column names in table
# f = cur.execute('SELECT name FROM sqlite_master ')
# printer(f)

# query SQLITE_MASTER table?
# n = cur.execute('SELECT * FROM sqlite_master')
# printer(n)

# # everything abt the tables
# k = cur.execute("SELECT name FROM sqlite_master " )
# k = cur.execute("SELECT sql FROM sqlite_master where type = 'table' " )
# k = cur.execute("SELECT sql FROM sqlite_master  " )
# printer(k)

# keyword search:
# printer(search_id('01001001'))
# keyword = "'%in the beginning %'"
# kw = cur.execute(f"SELECT * FROM t_kjv  where t like '%in the beginning %'")  
# kw = cur.execute(f'SELECT * FROM t_kjv  where t like {keyword} ')  
# keyword = "in the beginning "
# kw = cur.execute(f'SELECT * FROM t_kjv  where t like "%{keyword}%" ')  
# printer(kw)
keyword = "Blessed are the "
# printer(search_keyword(keyword))
print(search_keyword(keyword))

# bookid = 0
# print(get_bookname(bookid))