# import sqlite3
# from flask import g
# import os

# DATABASE = 'data.db'

# CREATE_TABLE = "Create table if not exists accounts(id integer primary key, user text, userpass text);"

# ADD_ACCOUNT = 'insert into accounts(user, userpass) values(?,?);'

# GET_ACCOUNT_BY_NAME = 'select * from accounts where user = ?;'

# CREATE_SONGS_TABLE = ""


# # connecting to db
# def flask_get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(DATABASE)
#         g.db.row_factory = sqlite3.Row
#         print("Connected to database:", DATABASE)
#     return g.db

# def flask_close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# # accounts
# def create_tables():
#     if not os.path.exists(DATABASE):
#         connection = sqlite3.connect(DATABASE)
#         with connection:
#             connection.execute(CREATE_TABLE)
#         connection.close()
#         print("Database and table created.")
#     else:
#         print("Database already exists.")


# def add_account(connection, user, userpass):
#     with connection:
#         connection.execute(ADD_ACCOUNT, (user, userpass))


# def get_account_by_name(connection, name):
#     with connection:
#         return connection.execute(GET_ACCOUNT_BY_NAME, (name,)).fetchall()


# class AccountCreation:
#     def __init__(self, username, password, connection):
#         self.username = username
#         self.password = password
#         self.connection = connection

#     def account_exists(self):
#         accounts = get_account_by_name(self.connection, self.username)
#         return bool(accounts)

#     def check_correct_password(self):
#         accounts = get_account_by_name(self.connection, self.username)
#         if accounts and accounts[0]['userpass'] == self.password:
#             return True
#         return False

#     def signup(self):
#         add_account(self.connection, self.username, self.password)

# # playlists