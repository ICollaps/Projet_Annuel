from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/health')
def health():
    return 'Hello, bro!'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)