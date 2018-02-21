import mysql.connector
from fuzzywuzzy import process


def name_matcher(name1, name2, total):
    # startTime = time.time() * 1000
    n = []
    n.append(name2.upper())
    match = process.extract(name1.upper(), n, limit=3)[0][1]
    score = (match / 100) * total
    # print('name_matcher ', time.time() * 1000 - startTime)
    return score

def checker(field1, field2,  score, ad):
    # startTime = time.time() * 1000
    if field1 == field2 == '':
        return False, score
    if field1 == field2:
        score = score + ad
        # print('checker ', time.time() * 1000- startTime)
        return True, score
    # print('checker ', time.time() * 1000 - startTime)
    return False, score

def field_checker(obj1, obj2, score, change):
    # startTime = time.time() * 1000
    name1 = obj1[3]
    name2 = obj2[3]
    name = score
    score = 0
    flag = 0
    ch, score = checker(obj1[8], obj2[8], score=score, ad=20)
    if not ch:
        change = change + 20
        name = name_matcher(name1, name2, change)
    else:
        flag = flag + 1
    ch, score = checker(obj1[20], obj2[20], score=score, ad=10)
    if not ch:
        change = change + 10
        name = name_matcher(name1, name2, change)
    ch, score = checker(obj1[14], obj2[14], score=score, ad=5)
    if not ch:
        change = change + 5
        name = name_matcher(name1, name2, change)
    ch, score = checker(obj1[27], obj2[27], score=score, ad=10)
    if not ch:
        change = change + 10
        name = name_matcher(name1, name2, change)
    ch, score = checker(obj1[11], obj2[11], score=score, ad=15)
    if not ch:
        change = change + 15
        name = name_matcher(name1, name2, change)
    else:
        flag = flag + 1
    # print('field_checkr ', time.time() * 1000 - startTime)
    return score+name, flag

def get_query(n, m):
    query = 'SELECT * FROM docs WHERE id BETWEEN {}'.format(n) + ' AND {}'.format(m)
    return query


def compare_self(cursor):
    rows = cursor.fetchall()
    for row1 in rows:
        for row2 in rows:
            if row1[0] != row2[0]:
                name = name_matcher(row1[3], row2[3], 40)
                if 16 < name < 32:
                    if row1[11] == row2[11] or row1[8] == row2[8]:
                        score, flag = field_checker(row1, row2, name, 40)
                        if score >= 90 or flag > 0:
                            pass
                elif name >= 32:
                    score, flag = field_checker(row1, row2, name, 40)
                    if score >= 90 or flag > 0:
                        pass


def compare(cursor1, cursor2):
    rows1 = cursor1.fetchall()
    rows2 = cursor2.fetchall()
    for row1 in rows1:
        for row2 in rows2:
            name = name_matcher(row1[3], row2[3], 40)
            if 16 < name < 32:
                if row1[11] == row2[11] or row1[8] == row2[8]:
                    score, flag = field_checker(row1, row2, name, 40)
                    if score >= 90 or flag > 0:
                        pass
            elif name >= 32:
                score, flag = field_checker(row1, row2, name, 40)
                if score >= 90 or flag > 0:
                    pass


con = mysql.connector.connect(user='root',
                              password='idhant',
                              host='127.0.0.1',
                              database='CSV_DB')

query = 'SELECT * FROM docs'
cursor = con.cursor()
cursor.execute(query)
row = cursor.fetchone()
cursor.fetchall()
count = cursor.rowcount
x = 1
cursors = []
while x <= count:
    cursor.execute(get_query(x, x + 1000))
    cursors.append(cursor.fetchall())
    input('first')
    if x+1000 < count:
        x = x + 1000
    else:
        cursor.execute(get_query(x, count))
        cursors.append(cursor.fetchall())
        input('last')
        x = x + 1000
con.close()
