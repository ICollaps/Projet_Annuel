from tokenize import String
from flask import Flask, redirect, url_for, render_template , request , flash , Blueprint , abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import numpy as np
import pandas as pd
import io

from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from functools import wraps
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

def medecin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'médecin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function




app = Flask(__name__)

app.config['LOGIN_VIEW'] = 'login'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Annual_Project' 
app.config['SECRET_KEY'] = 'some_secret_key'

client = MongoClient(app.config['MONGO_URI'])
db = client.get_default_database()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class UserObj:
    def __init__(self, user):
        self.id = str(user['_id'])
        self.username = user['username']
        self.role = user['role']
        self.is_active = True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return UserObj(user)
    




def convert_numpy_int64(document):
        for key, value in document.items():
            if isinstance(value, np.int64):
                document[key] = value.item()
        return document




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            user_obj = UserObj(user)
            login_user(user_obj)
            flash('Vous êtes connecté avec succès !', 'success')
            # if user['role'] == 'admin':
            #     return redirect(url_for('admin'))
            # else:
            #     return redirect(url_for('menu'))
            redirect(url_for('menu'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", 'danger')

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté avec succès.', 'success')
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():

    doctors = db.users.find({'role': 'médecin'})
    
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        hashed_password = generate_password_hash(password, method='sha256')


        existing_user = db.users.find_one({'username': username})
        if existing_user:
            flash("Nom d'utilisateur déjà pris, veuillez en choisir un autre.", 'danger')
            return redirect(url_for('register'))
        
        

        if role == 'patient' :
            doctor_name = request.form.get('doctor_name_select')
            new_user = {'username': username, 'password': hashed_password, 'role': role , 'doctor_name' : doctor_name , 'email' :  email , 'first_name' : first_name , 'last_name' : last_name}
        elif role == 'médecin' :
            new_user = {'username': username, 'password': hashed_password, 'role': role , 'email' :  email , 'first_name' : first_name , 'last_name' : last_name}
        elif role == 'admin' :
            new_user = {'username': username, 'password': hashed_password, 'role': role}

        db.users.insert_one(new_user)
        flash("Inscription réussie ! Veuillez vous connecter.", 'success')
        return redirect(url_for('login'))

    return render_template('register.html' , doctors=doctors)



@app.route('/admin')
@login_required
@admin_required
def admin():
    users = db.users.find()
    predictions = db.predictions.find()
    return render_template('admin.html', users=users , predictions=predictions)




@app.route('/delete_users', methods=['POST'])
@login_required
@admin_required  # Make sure only admin can delete users
def delete_users():
    # Getting the list of user IDs from the form
    user_ids = request.form.getlist('user_ids')

    # Deleting the users by their _id
    for user_id in user_ids:
        db.users.delete_one({"_id": ObjectId(user_id)})
    
    flash(f"{len(user_ids)} utilisateur(s) ont été supprimé(s) avec succès.", "success")
    return redirect(url_for('admin'))


@app.route('/delete_predictions', methods=['POST'])
@login_required
@admin_required  # Make sure only admin can delete predictions
def delete_predictions():
    # Getting the list of prediction IDs from the form
    prediction_ids = request.form.getlist('prediction_ids')

    # Deleting the predictions by their _id
    for prediction_id in prediction_ids:
        db.predictions.delete_one({"_id": ObjectId(prediction_id)})

    flash(f"{len(prediction_ids)} prédiction(s) ont été supprimée(s) avec succès.", "success")
    return redirect(url_for('admin'))








@app.route('/menu')
@login_required
def menu():
    if current_user.role == 'patient':
        return render_template('menu_patient.html')
    elif current_user.role == 'médecin':
        return render_template('menu_medecin.html')
    elif current_user.role == 'admin':
        return render_template('menu_admin.html')
    else:
        return "Erreur : rôle non reconnu"
    

@app.route('/history')
@login_required
def history():
    return render_template('history.html')






model = joblib.load("model/trained_models/best_model.pkl")


@app.route('/')
def index():
    return render_template('welcome.html')


@app.route('/medecin')
@login_required
def medecin():
    return render_template('medecin.html')


@app.route('/medecin/predictions')
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
                
    # Formatage des prédictions
    formatted_predictions = [{
        'id': str(p['_id']),
        'user_id': p['user_id'],
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
        'probability': p['probability']
    } for p in predictions]
    
    ages = [p['Age'] for p in formatted_predictions]

    return render_template('prediction_analysis.html', predictions=formatted_predictions, ages=ages)



@app.route('/medecin/upload', methods=['GET', 'POST'])
@login_required
@medecin_required
def medecin_upload():
    if request.method == 'POST':
        file = request.files['file']
        # Read it as a pandas DataFrame:
        import pandas as pd
        import io
        file_stream = io.StringIO(file.read().decode('utf-8'))
        df = pd.read_csv(file_stream)
        predictions = []

        for i in range(len(df)):
            input_values = [df["PRG"][i], df["PL"][i], df["PR"][i], df["SK"][i], df["TS"][i], df["M11"][i], df["BD2"][i], df["Age"][i], df["Insurance"][i]]
            user_display = int(df["ID"][i])
            prediction = model.predict([input_values])[0]
            probabilities = model.predict_proba([input_values])[0]
            probability = round(probabilities[prediction] * 100, 2)

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
                'probability': float(probability)
            }

            predictions.append(new_prediction)

        # Insérer toutes les nouvelles prédictions dans la base de données MongoDB
        db.predictions.insert_many(predictions)

        return render_template('medecin_multi_results.html', predictions=predictions)

    else:
        return render_template('medecin_upload.html')




# class Prediction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     PRG = db.Column(db.Float, nullable=False)
#     PL = db.Column(db.Float, nullable=False)
#     PR = db.Column(db.Float, nullable=False)
#     SK = db.Column(db.Float, nullable=False)
#     TS = db.Column(db.Float, nullable=False)
#     M11 = db.Column(db.Float, nullable=False)
#     BD2 = db.Column(db.Float, nullable=False)
#     Age = db.Column(db.Float, nullable=False)
#     Insurance = db.Column(db.Float, nullable=False)
#     prediction = db.Column(db.Integer, nullable=False)
#     probability = db.Column(db.Float, nullable=False)

#     user = db.relationship('User', backref=db.backref('predictions', lazy=True))




@app.route('/health')
@login_required
def health():
    return render_template('user_input.html')


@app.route('/health/predict', methods=['POST'])
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

    input_values = [PRG, PL, PR, SK, TS, M11, BD2, Age, Insurance]

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
        'probability': probability
    }


    new_prediction = convert_numpy_int64(new_prediction)
    db.predictions.insert_one(new_prediction)

    return render_template('prediction_result.html', prediction=prediction, probability=probability, variables=variables)



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000,debug=True)