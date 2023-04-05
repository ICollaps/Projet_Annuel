from flask import Flask, redirect, url_for, render_template , request
import joblib

app = Flask(__name__)

model = joblib.load("model/trained_models/best_model.pkl")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return render_template('form.html')

@app.route('/health/predict', methods=['POST'])
def predict():
    input_data = request.form['input_data']
    input_values = list(map(float, input_data.split(',')))

    prediction = model.predict([input_values])[0]
    return f'La prédiction du modèle est : {prediction}'










if __name__ == '__main__':
    app.run(debug=True)