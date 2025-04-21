from flask import Flask, request, redirect, render_template_string
import hashlib
import time

app = Flask(__name__)

# A dictionary to store the mapping between short URLs and original URLs
url_mapping = {}
# Home page route to render the input form for the URL
@app.route('/')
def home():
    return render_template_string('''
        <h1>URL Shortener</h1>
        <form method="POST" action="/shorten">
            <label for="url">Enter URL to shorten:</label>
            <input type="text" name="url" id="url" required>
            <button type="submit">Shorten</button>
        </form>
    ''')
# Route to handle the URL shortening process
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    
    # Create a unique hash for the original URL (we'll use hashlib)
    unique_hash = hashlib.md5(f'{original_url}{time.time()}'.encode()).hexdigest()[:6]
    
    # Save the mapping of the hash to the original URL
    url_mapping[unique_hash] = original_url
    
    short_url = f'http://localhost:5000/{unique_hash}'
    
    return f'<h1>Shortened URL:</h1><a href="{short_url}">{short_url}</a>'
# Route to handle redirection to the original URL
@app.route('/<short_hash>')
def redirect_to_url(short_hash):
    original_url = url_mapping.get(short_hash)
    
    if original_url:
        return redirect(original_url)
    else:
        return '<h1>404 - URL not found!</h1>', 404
if __name__ == '__main__':
    app.run(debug=True)