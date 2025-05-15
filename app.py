from flask import Flask, render_template, request, jsonify, Response
from songconv import song_importer, get_audio
import requests

app = Flask(__name__)

# song searching

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result')
def search():

    title = request.args.get('title')

    result = song_importer(title)
    print(result.title)
    print(result.possible_titles)
    if result.title != 'ERROR':
        return render_template('result.html', results = result)
    else:
        return render_template('error.html', song_suggestions = result.possible_titles)

# route to retrieve audio after page has loaded
@app.route('/retrieve-audio', methods=['POST']) 
def retrieve_audio():
    data = request.get_json()
    title = data.get('title')
    artist = data.get('artist')
    print(title, artist)
    get_audio(title, artist)

    return jsonify({'url': f'static/downloads/{title}.webm'})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)