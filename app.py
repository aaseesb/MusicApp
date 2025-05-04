from flask import Flask, render_template, request
from engine import Engine

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    engine = Engine()
    item = engine.search(title, artist)
    return render_template('search.html', results=item)


if __name__ == '__main__':
    app.run(debug=True)