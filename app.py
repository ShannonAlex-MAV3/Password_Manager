#Author MAV3


import db
from custom_lib import login_required
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet


# configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # get current user id
    user_id = int(session["user_id"])

    # fetch data from passswords tabel
    Rows = db.fetch_saved_data(user_id)

    # no.of passwords
    length = len(Rows)

    # data_list with decrypted passwords
    Data_list = []
   
    for i in range(length):
        # configure key fernet
        fernet = Fernet(Rows[i][5])
        ecrypt_pass = Rows[i][4]

        # decrypt password
        password = fernet.decrypt(ecrypt_pass).decode()

        # temp list
        temp = []

        # append data to temp list
        temp.append(int(Rows[i][0]))
        temp.append(int(Rows[i][1]))
        temp.append(Rows[i][2])
        temp.append(Rows[i][3])
        temp.append(password)

        # append data to Data_list
        Data_list.append(temp)


    return render_template("index.html",Data_list=Data_list, length=length)


@app.route("/add_password", methods=["GET", "POST"])
@login_required
def add_password():

    # check for post request
    if request.method == "POST":
        website = request.form.get("website")
        username = request.form.get("username")
        password = request.form.get("password")

        # chcek if fields are empty
        if not website or not username or not password:
            flash("Field Empty!")
            return redirect("/")

        # configure fernet
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # encrypt password
        encrypt_pass = fernet.encrypt(password.encode())

        # get current user id
        user_id = session["user_id"]

        # add password to database
        db.add_pass(user_id,website,username,encrypt_pass,key)


        flash("Saved Passwords Successfully!")
        return redirect("/")


    else:
        flash("Error Try Again!")
        return redirect("/")


@app.route("/update", methods=["GET", "POST"])
@login_required
def edit():
    # check if post method is used
    if request.method == "POST":
        pass_id = request.form.get("pass_id")
        website = request.form.get("website")
        username = request.form.get("username")
        password = request.form.get("password")

        # check if declared variables are empty
        if not pass_id:
            return redirect("/")
        if not website or not username or not password:
            flash("Field Empty")
            return redirect("/")

        # configure fernet
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # encrypt password
        encrypt_pass = fernet.encrypt(password.encode())
        # update data in table
        
        # update passwords table
        try:
            db.update_pass(pass_id,website,username,encrypt_pass,key)
            flash("Updated successfully!")
            return redirect("/")
        except:
            flash("Error Try Again")
            return redirect("/")
        
    # if get method is used
    else:
        return redirect("/")

@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():

    # check for post request
    if request.method == "POST":
        pass_id = request.form.get("delete")
        # delete password details
        db.delete_pass(pass_id)
        flash("Deleted sucessfully!")
        return redirect("/")

    else:
         return("/")


@app.route("/login", methods=["GET","POST"])
def login():
    #log user

    #clear any existing user id
    session.clear()

    # check for POST request
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        #if no username entered , print error
        if not username:
            flash("Username field empty")
            return render_template("login_and_reg.html")

        # if no password typed , print error
        if not password:
            flash("Password field empty")
            return render_template("login_and_reg.html")

        #search database for username
        row = db.search_user(username)

        #check if username exists
        if len(row) != 1 or not check_password_hash(row[0][2],password):
            flash("Username and/or Password Invalid")
            return render_template("login_and_reg.html")

        session["user_id"] = row[0][0]

        #redirect to home page
        return redirect("/")

    # if request done via GET
    else:
        return render_template("login_and_reg.html")

@app.route("/logout")
@login_required
def logout():
    # clear session or forget user
    session.clear()

    flash("Logged out sucessfully!")
    return render_template("login_and_reg.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # add new user to system
    
    # check for post request method
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirmation")

        # check if fields are empty and if pass match with confirm_pass
        if not username:
            flash("Username field empty")
            return render_template("login_and_reg.html")

        # search database for username
        row = db.search_user(username)

        # check if username exists
        if row:
            flash("Username Already Exists")
            return render_template("login_and_reg.html")
                   
        if not password:
            flash("Password field empty")
            return render_template("login_and_reg.html")

        if password != confirm_pass:
            flash("passwords do not match")
            return render_template("login_and_reg.html")

        # create hash for password
        hash = generate_password_hash(password)
        print("sucess")
        # if all above is validated add user
        try:
            db.add_user(username, hash)
            flash("Registered Successfully!")
            print("suc2")
            return render_template("login_and_reg.html")
        except:
            flash("Error Please Try Again!")  
            return render_template("login_and_reg.html")  

    # if get request is used
    else:
        return render_template("login_and_reg.html")

