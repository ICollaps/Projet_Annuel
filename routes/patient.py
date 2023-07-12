from flask import Blueprint, render_template , abort , redirect , request , flash , url_for , make_response
from flask_login import login_required , current_user
from bson import ObjectId

from utils.functions import validate_input , convert_numpy_int64 , send_email , generate_html_table
from utils.config import model , db


patient_bp = Blueprint('patient_bp', __name__)


@patient_bp.route('/health')
@login_required
def health():
    return render_template('user_input.html')




@patient_bp.route('/health/predict', methods=['POST'])
@login_required
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
    last_name = db.users.find_one({'_id': ObjectId(current_user.get_id())})['last_name']
    first_name = db.users.find_one({'_id': ObjectId(current_user.get_id())})['first_name']

    input_values = [PRG, PL, PR, SK, TS, M11, BD2, Age, Insurance]

    # Valider les données
    if not validate_input(input_values):
        flash('Invalid data.', 'error')
        return redirect(url_for('patient_bp.health'))

    prediction = model.predict([input_values])[0]
    probabilities = model.predict_proba([input_values])[0]
    probability = round(probabilities[prediction] * 100, 2)

    if prediction == 0 :
        prediction = 'négatif'
    else:
        prediction = 'positif'

    variables = [
        {'name': 'PRG', 'value': PRG, 'description': 'Description pour PRG'},
        {'name': 'PL', 'value': PL, 'description': 'Description pour PL'},
        {'name': 'PR', 'value': PR, 'description': 'Description pour PR'},
        {'name': 'SK', 'value': SK, 'description': 'Description pour SK'},
        {'name': 'TS', 'value': TS, 'description': 'Description pour TS'},
        {'name': 'M11', 'value': M11, 'description': 'Description pour M11'},
        {'name': 'BD2', 'value': BD2, 'description': 'Description pour BD2'},
        {'name': 'Age', 'value': Age, 'description': 'Description pour Age'},
        {'name': 'Insurance', 'value': Insurance, 'description': 'Description pour Insurance'}
    ]

    # Enregistrer la prédiction dans la base de données MongoDB
    new_prediction = {
        'user_id': current_user.get_id(),
        'PRG': PRG,
        'PL': PL,
        'PR': PR,
        'SK': SK,
        'TS': TS,
        'M11': M11,
        'BD2': BD2,
        'Age': Age,
        'Insurance': Insurance,
        'prediction': prediction,
        'probability': probability,
        'name' : f'{last_name} {first_name}'
    }


    

    new_prediction = convert_numpy_int64(new_prediction)
    db.predictions.insert_one(new_prediction)

      # Retrieve the user's email from the database and the from adress
    user_email = db.users.find_one({'_id': ObjectId(current_user.get_id())})['email']
    from_addr="annual.project.esgi@gmail.com"
    password = "hnnsrzdbpzdvypwy"
    # Create the email message
    subject = "New Health Prediction"
    message = f"A new health prediction has been made for your account. The prediction is {prediction} with a probability of {probability}."
    
    # Send the email
    send_email(subject, message, from_addr, user_email, password, variables)


    return render_template('prediction_result.html', prediction=prediction, probability=probability, variables=variables)