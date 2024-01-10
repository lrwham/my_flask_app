#!/usr/bin/env python3

from flask import Flask, request, send_file, render_template, jsonify
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

matplotlib.use('Agg')

def generate_word_cloud(words_with_weights):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(words_with_weights)

    img = io.BytesIO()  # Create an in-memory bytes buffer
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(img, format='png')  # Save the plot to the bytes buffer
    img.seek(0)  # Rewind the buffer
    plt.close()
    
    return img

@app.route('/generate_wordcloud', methods=['POST'])
def wordcloud_api():
    data = request.json
    print (data)
    img = generate_word_cloud(data)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False)
