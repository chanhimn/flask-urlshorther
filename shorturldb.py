import sqlite3
from sqlite3 import Error

database = "SHORTURL.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_url_table():
    try:
        conn = create_connection(database)
        sql_create_url_table = """ CREATE TABLE IF NOT EXISTS url (
                                        rid INTEGER PRIMARY KEY,
                                        short text UNIQUE,
                                        link text
                                    ); """
        cur = conn.cursor()
        cur.execute(sql_create_url_table)
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("create_url_table", e)
        return None

def insert_url_record(shortlink):
    try:
        conn = create_connection(database)
        sql = ''' INSERT INTO url(short, link)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, shortlink)
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("insert_shortcut", e)
        return None

def update_url_record(shortlinkid):
    try:
        conn = create_connection(database)
        sql = ''' UPDATE url
                  SET short = ?,
                      link = ?
                  WHERE rid = ?'''
        cur = conn.cursor()
        cur.execute(sql, shortlinkid)
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("update_shortcut", e)
        return None

def update_url_record_by_short(shortlink):
    try:
        conn = create_connection(database)
        sql = ''' UPDATE url
                  SET link = ?
                  WHERE short = ?'''
        cur = conn.cursor()
        cur.execute(sql, shortlink)
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("update_shortcut", e)
        return None

def delete_url_record_by_rid(rid):
    try:
        conn = create_connection(database)
        sql = '''DELETE FROM url WHERE rid=?'''
        cur = conn.cursor()
        print("chn1")
        cur.execute(sql, (rid,))
        print("chn2")
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("delete_shortcut_record", e)
        return None

def delete_url_record_by_short(short):
    try:
        conn = create_connection(database)
        sql = '''DELETE FROM url WHERE short=?'''
        cur = conn.cursor()
        cur.execute(sql, (short,))
        cur.close()
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Error as e:
        print("delete_shortcut_record", e)
        return None

def execute_sql(sql):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    data = None
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except sqlite3.IntegrityError:
        print("Repeated Data\n")
    except:
        print("SQL Error: ", sys.exc_info()[0])
    conn.commit()
    cursor.close()
    conn.close()
    return data

def main():
    
    create_url_table()
    insert_url_record(('b', 'https://www.bing.com/'))
    insert_url_record(('d', 'https://duckduckgo.com/'))
    insert_url_record(('g', 'https://www.google.com.sg'))
    insert_url_record(('y', 'https://sg.yahoo.com/?p=us'))
##    update_url_record(database, ('b', 'https://www.bing.com/', 3))
##    update_url_record_by_short(database, ('sg.google.com', 'g'))
##    delete_url_record_by_rid(database, (1,))
##    delete_url_record_by_short(database, ('g',))

if __name__ == '__main__':
    main()
