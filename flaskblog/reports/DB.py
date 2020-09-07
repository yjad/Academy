import sqlite3
from sqlalchemy.sql import text
from flaskblog.reports.config import config
from flaskblog import db

MEETING_TABLE = "meetings"
ATTENDEES_TABLE = "attendees"


# def open_db():
#     connection = sqlite3.Connection(config.get("DB_FILE_NAME"))
#     cursor = connection.cursor()
#     return connection, cursor


def create_tables():
    cmd = f'CREATE TABLE IF NOT EXISTS {MEETING_TABLE}' \
          f'(uuid TEXT NOT NULL PRIMARY KEY,' \
          f'id INTEGER ,' \
          f'host_id	TEXT,' \
          f'type	INTEGER,' \
          f'topic	TEXT,' \
          f'user_name	TEXT,' \
          f'user_email TEXT,' \
          f'start_time TEXT,' \
          f'end_time	TEXT,' \
          f'duration	INTEGER,' \
          f'total_minutes	INTEGER,' \
          f'participants_count INTEGER)'

    db.engine.execute(cmd)

    db.engine.execute(f'CREATE TABLE IF NOT EXISTS {ATTENDEES_TABLE}'
                   '(meeting_uuid TEXT,'
                   'id TEXT ,'
                   'user_id TEXT,'
                   'name TEXT,'
                   'user_email TEXT,'
                   'join_time TEXT,'
                   'leave_time TEXT,'
                   'duration INTEGER,'
                   'attentiveness_score TEXT)')
    return


# def close_db(cursor):
#     cursor.close()


def insert_row(table_name, rec):
    keys = ','.join(rec.keys())
    question_marks = ','.join(list('?' * len(rec)))
    values = tuple(rec.values())
    try:
        db.engine.execute('INSERT INTO ' + table_name + ' (' + keys + ') VALUES (' + question_marks + ')', values)
        #db.engine.commit()
        return 0
    #except sqlite3.Error as er:
    except :    # already exist
        #print('SQLite error: %s' % (' '.join(er.args)))
        #print("Exception class is: ", er.__class__)
        #print('SQLite traceback: ')
        #exc_type, exc_value, exc_tb = sys.exc_info()
        #print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return -1


def insert_row_meeting(rec):
    return insert_row(MEETING_TABLE, rec)


def insert_row_attendees(rec):
    return insert_row(ATTENDEES_TABLE, rec)


def exec_query(cmd):
    rows = db.engine.execute(cmd)
    #rows = db.engine.fetchall()
    return rows


def get_last_meeting_date():
    #conn, cursor = open_db()
    rows = db.engine.execute('SELECT start_time from meetings order by start_time DESC LIMIT 1')
    #rows = db.engine.fetchall()
    #close_db(cursor)
    for r in rows:
        print (r)
        print (r[0])
        print (r[0][:10])
        return r[0][:10]


def get_col_names(sql):
    get_column_names = db.engine.execute(sql + " limit 1")
    col_name = [i[0] for i in get_column_names.description]
    return col_name
