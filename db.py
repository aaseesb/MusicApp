import sqlite3
from flask import g

DATABASE = 'data.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# storing create table, insert, and retrieve commands to a variable in python
CREATE_TABLE = "Create table if not exists accounts(id integer primary key, user text, userpass text);"

ADD_ACCOUNT = 'insert into accounts(user, userpass) values(?,?);'

GET_ACCOUNT_BY_NAME = 'select * from accounts where user = ?;'

def create_tables(connection):
    with connection:
        connection.execute(CREATE_TABLE)

def add_account(connection, user, userpass):
    with connection:
        connection.execute(ADD_ACCOUNT, (user, userpass))

def get_account_by_name(connection, name):
    with connection:
        return connection.execute(GET_ACCOUNT_BY_NAME, (name,)).fetchall()