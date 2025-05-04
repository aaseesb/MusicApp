from flask import Flask, render_template, request
from engine import Engine

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    title = request.args.get('title')
    print(title)
    artist = request.args.get('artist')
    print(artist)
    
    results = []
    engine = Engine()
    results = engine.search(title, artist)
    # for item in results:
    #     print(item.title, " ", item.image)
    
    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)