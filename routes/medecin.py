from flask import Blueprint, render_template , abort , redirect , request , flash , url_for , make_response
from flask_login import login_required , current_user
from functools import wraps
import numpy as np
import pandas as pd
import io
import csv

# from app import db , model
from utils.functions import validate_input , convert_numpy_int64
from utils.config import db , model

medecin_bp = Blueprint('medecin_bp', __name__)


def medecin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'médecin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


@medecin_bp.route('/medecin')
@login_required
def medecin():
    return render_template('medecin.html')



@medecin_bp.route('/medecin/predictions')
@login_required
@medecin_required
def medecin_predictions():
    # Récupère toutes les prédictions de la collection 'predictions'
    predictions_cursor = db.predictions.find()
    
    # Transforme le curseur en liste de dictionnaires
    predictions = list(predictions_cursor)

    # Convertit les données numpy en données python standard
    for p in predictions:
        for key, value in p.items():
            if isinstance(value, np.int64):
                p[key] = int(value)

    # Count number of patients with prediction 1 and 0
    pred_counts = [p['prediction'] for p in predictions]
    counts = [pred_counts.count(x) for x in set(pred_counts)]

    # Formatage des prédictions
    formatted_predictions = [{
        'id': str(p['_id']),
        'PRG': p['PRG'],
        'PL': p['PL'],
        'PR': p['PR'],
        'SK': p['SK'],
        'TS': p['TS'],
        'M11': p['M11'],
        'BD2': p['BD2'],
        'Age': p['Age'],
        'Insurance': p['Insurance'],
        'prediction': p['prediction'],
        'probability': p['probability'],
        'name' : p['name']
    } for p in predictions]

    ages = [p['Age'] for p in formatted_predictions]

    return render_template('prediction_analysis.html', predictions=formatted_predictions, ages=ages, prediction_counts=counts)



@medecin_bp.route('/medecin/form')
@login_required
def med_form():

    patients = db.users.find({'role': 'patient'})
    print(patients)
    return render_template('med_user_input.html' , patients=patients)


@medecin_bp.route('/medecin/predict', methods=['POST'])
@login_required
def med_predict():
    PRG = float(request.form['PRG'])
    PL = float(request.form['PL'])
    PR = float(request.form['PR'])
    SK = float(request.form['SK'])
    TS = float(request.form['TS'])
    M11 = float(request.form['M11'])
    BD2 = float(request.form['BD2'])
    Age = float(request.form['Age'])
    Insurance = float(request.form['Insurance'])
    patient_name = str(request.form['patient_name_select'])

    input_values = [PRG, PL, PR, SK, TS, M11, BD2, Age, Insurance]

    # Valider les données
    if not validate_input(input_values):
        flash('Invalid data.', 'error')
        return redirect(url_for('patient_bp.health'))

    prediction = model.predict([input_values])[0]
    probabilities = model.predict_proba([input_values])[0]
    probability = round(probabilities[prediction] * 100, 2)

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
        'name' : patient_name
    }


    

    new_prediction = convert_numpy_int64(new_prediction)
    db.predictions.insert_one(new_prediction)


    return render_template('prediction_result.html', prediction=prediction, probability=probability, variables=variables)


@medecin_bp.route('/medecin/upload', methods=['GET', 'POST'])
@login_required
@medecin_required
def medecin_upload():
    if request.method == 'POST':
        file = request.files['file']
        # Read it as a pandas DataFrame:
        
        file_stream = io.StringIO(file.read().decode('utf-8'))
        df = pd.read_csv(file_stream)


        # Check if the DataFrame has the right columns
        expected_columns = ['ID', 'PRG', 'PL', 'PR', 'SK', 'TS', 'M11', 'BD2', 'Age', 'Insurance' , 'Name']
        if list(df.columns) != expected_columns:
            flash( 'Le format du fichier est invalide. Veuillez vous assurer que les colonnes sont : ' + ', '.join(expected_columns) , 'danger')
            return redirect(url_for('medecin_bp.medecin_upload'))
        
        
        predictions = []

        for i in range(len(df)):

            

            input_values = [df["PRG"][i], df["PL"][i], df["PR"][i], df["SK"][i], df["TS"][i], df["M11"][i], df["BD2"][i], df["Age"][i], df["Insurance"][i]]
            
            # Valider les données
            if not validate_input(input_values):
                flash('Invalid data.', 'danger')
                return redirect(url_for('medecin_bp.medecin_upload'))
            
            

        
    
            user_display = int(df["ID"][i])
            prediction = model.predict([input_values])[0]
            probabilities = model.predict_proba([input_values])[0]
            probability = round(probabilities[prediction] * 100, 2)
            name = df["Name"][i]

            # Créer une nouvelle prédiction
            new_prediction = {
                'PRG': int(df["PRG"][i]),  # Conversion en entier standard
                'PL': int(df["PL"][i]),  # Conversion en entier standard
                'PR': int(df["PR"][i]),  # Conversion en entier standard
                'SK': int(df["SK"][i]),  # Conversion en entier standard
                'TS': int(df["TS"][i]),  # Conversion en entier standard
                'M11': int(df["M11"][i]),  # Conversion en entier standard
                'BD2': int(df["BD2"][i]),  # Conversion en entier standard
                'Age': int(df["Age"][i]),  # Conversion en entier standard
                'Insurance': int(df["Insurance"][i]),  # Conversion en entier standard
                'prediction': int(prediction),
                'probability': float(probability),
                'name' : str(name)
            }

            predictions.append(new_prediction)

        # Insérer toutes les nouvelles prédictions dans la base de données MongoDB
        db.predictions.insert_many(predictions)

        return render_template('medecin_multi_results.html', predictions=predictions)

    else:
        return render_template('medecin_upload.html')
    



@medecin_bp.route('/medecin/predictions/export')
@login_required
@medecin_required
def export_predictions():
    # Fetch predictions from database
    predictions_cursor = db.predictions.find()
    predictions = list(predictions_cursor)

    # Prepares data and column names
    data = [{k: v if not isinstance(v, np.int64) else int(v) for k, v in d.items()} for d in predictions]
    column_names = data[0].keys()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(column_names)  # Write column names
    cw.writerows([list(d.values()) for d in data])  # Write data

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=predictions_export.csv"
    output.headers["Content-type"] = "text/csv"

    return output