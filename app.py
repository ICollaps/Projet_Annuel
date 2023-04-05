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
    PRG = float(request.form['PRG'])
    PL = float(request.form['PL'])
    PR = float(request.form['PR'])
    SK = float(request.form['SK'])
    TS = float(request.form['TS'])
    M11 = float(request.form['M11'])
    BD2 = float(request.form['BD2'])
    Age = float(request.form['Age'])
    Insurance = float(request.form['Insurance'])

    input_values = [PRG, PL, PR, SK, TS, M11, BD2, Age, Insurance]

    prediction = model.predict([input_values])[0]
    return f'La prédiction du modèle est : {prediction}'










if __name__ == '__main__':
    app.run(debug=True)