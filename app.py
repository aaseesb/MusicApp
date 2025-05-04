from flask import Flask, render_template, request
from engine import Engine

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        engine = Engine()
        results = engine.search(title, artist)
    return render_template('home.html', results = results)

if __name__ == '__main__':
    app.run(debug=True)