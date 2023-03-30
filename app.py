from flask import Flask

app = Flask(__name__)

@app.route('/health')
def index():
    return 'Hello, bro!'

if __name__ == '__main__':
    app.run(debug=True)