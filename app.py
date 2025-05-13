from flask import Flask, render_template, request, redirect, session
import accounts
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

# song searching

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/result')
def search():
    title = request.args.get('title')


# song liking

@app.route('/likedsongs')
def likedsongs():
    return render_template('playlist.html')

@app.route('/addliked', methods=['POST'])
def addliked():
    # retrieve song and add to session playlist
    song = request.args.get('song')
    session['playlist'].append(song)

    # add to playlist data for javascript

    # reload same page
    return render_template('result.html', results=song, )


# account use

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
                session['username'] = username
                return redirect('/')
            else:
                message = "Incorrect password"
        else:
            message = "Account does not exist"

    return render_template("login.html", message = message)

@app.route('/signup', methods=['GET','POST'])
def signup():
    message = ""
    if request.method == 'POST':
        # retrieve username and password
        username = request.form.get('username')
        password = request.form.get('password')

        # create account object
        db = accounts.flask_get_db()
        account = accounts.AccountCreation(username, password, db)

        if account.account_exists():
            message = "Account already exists"
        else:
            account.signup()
            return redirect('/login')
    
    return render_template("signup.html", message = message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    accounts.create_tables()
    app.run(debug=True)