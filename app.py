from flask import Flask, render_template, request, redirect, session
from engine import Engine
import accounts

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/result')
def search():
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    engine = Engine()
    item = engine.search(title, artist)
    return render_template('result.html', results=item)


@app.route('/login', methods=['GET','POST'])
def login():
    message = ""
    if request.method == 'POST':
        # retrieve username and password
        username = request.form.get('username')
        password = request.form.get('password')

        # create account object
        db = accounts.flask_get_db()
        account = accounts.AccountCreation(username, password, db)

        if account.account_exists():
            if account.check_correct_password():
                # create a session with username since user was able to log in
                # session['username'] = username
                return redirect('/')
            else:
                message = "Incorrect password"
        else:
            message = "Account does not exist"

    return render_template("login.html", message = message)

"""
def signup():
    message = ""
    if request.method == 'POST':
        # retrieve username and password
        username = request.form.get('username')
        password = request.form.get('password')

        # create account object
        account = account.AccountCreation(username, password)

        if account.account_exists():
            message = "Account already exists"
        else:
            account.signup()
            return redirect('/login')
    
    return render_template("signup.html", message = message)
"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    accounts.create_tables()
    app.run(debug=True)