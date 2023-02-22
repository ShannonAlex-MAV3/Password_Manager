#Author MAV3

import sqlite3


#search user function
def search_user(username):

    #connect to database
    db = sqlite3.connect('app.db')

    # create cursor for db commands
    c = db.cursor()

    # execute query
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchall()

    db.commit()

    #close database
    db.close()

    return row

#fetch saved data from passwords table for a certain user function
def fetch_saved_data(user_id):

    db = sqlite3.connect('app.db')

    # create cursor for db commands
    c = db.cursor()

    # query
    c.execute("SELECT * FROM passwords WHERE user_id = ?", (user_id,))
    row = c.fetchall()

    db.commit()

    #close database
    db.close()

    return row

#add new user funtion
def add_user(name, hash):
    db = sqlite3.connect('app.db')

    # create cursor for db commands
    c = db.cursor()

    # query
    c.execute("INSERT INTO users (username,hash) VALUES (?, ?)", (name, hash))

    db.commit()

    #close database
    db.close()


# add new password to password table
def add_pass(user_id,website,username,encrypt_pass,key):
    db = sqlite3.connect("app.db")

    # create cursor for db commands
    c = db.cursor()

    # query
    c.execute("INSERT INTO passwords (user_id,website,username,encrypt_pass,key) VALUES (?, ?, ?, ?, ?)",(user_id,website,username,encrypt_pass,key))

    db.commit()

    # close db
    db.close()

# update password details in password table
def update_pass(pass_id,website,username,encrypt_pass,key):
    db = sqlite3.connect("app.db")

    # create cursor for db commands
    c = db.cursor()

    # query
    c.execute("UPDATE passwords SET website = (?), username = (?), encrypt_pass = (?), key = (?) WHERE pass_id = (?)", (website,username,encrypt_pass,key,pass_id))

    db.commit()

    # close db
    db.close()

# delete password from passwords table
def delete_pass(pass_id):
    db = sqlite3.connect("app.db")

    # create cursor for db commands
    c = db.cursor()

    # query
    c.execute("DELETE FROM passwords WHERE pass_id = (?)", (pass_id,))

    db.commit()

    # close db
    db.close()
