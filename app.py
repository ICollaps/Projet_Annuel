from tokenize import String
from flask import Flask, redirect, url_for, render_template , request , flash , Blueprint , abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from functools import wraps
from pymongo import MongoClient
from bson import ObjectId


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
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('menu'))
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password, method='sha256')

        existing_user = db.users.find_one({'username': username})
        if existing_user:
            flash("Nom d'utilisateur déjà pris, veuillez en choisir un autre.", 'danger')
            return redirect(url_for('register'))

        new_user = {'username': username, 'password': hashed_password, 'role': role}
        db.users.insert_one(new_user)
        flash("Inscription réussie ! Veuillez vous connecter.", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/admin')
@login_required
@admin_required
def admin():
    users = db.users.find()
    return render_template('admin.html', users=users)




@app.route('/delete_user/<user_id>')
@login_required
@admin_required  # Make sure only admin can delete users
def delete_user(user_id):
    # Deleting the user by its _id
    db.users.delete_one({"_id": ObjectId(user_id)})
    flash("L'utilisateur a été supprimé avec succès.", "success")
    return redirect(url_for('admin'))





@app.route('/menu')
@login_required
def menu():
    if current_user.role == 'patient':
        return render_template('menu_patient.html')
    elif current_user.role == 'médecin':
        return render_template('menu_medecin.html')
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


# @app.route('/medecin/predictions')
# @login_required
# @medecin_required
# def medecin_predictions():
    
#     predictions = Prediction.query.all()
#     formatted_predictions = []

#     for p in predictions:
#         formatted_predictions.append({
#             'id': p.id,
#             'user_id': p.user_id,
#             'PRG': p.PRG,
#             'PL': p.PL,
#             'PR': p.PR,
#             'SK': p.SK,
#             'TS': p.TS,
#             'M11': p.M11,
#             'BD2': p.BD2,
#             'Age': p.Age,
#             'Insurance': p.Insurance,
#             'prediction': int.from_bytes(p.prediction, byteorder='little'),
#             'probability': p.probability
#         })
    
#     ages = [p['Age'] for p in formatted_predictions]


#     return render_template('prediction_analysis.html', predictions=formatted_predictions , ages=ages)

# ########################################################################################################################

# @app.route('/medecin/upload', methods=['GET', 'POST'])
# @login_required
# @medecin_required
# def medecin_upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         # Read it as a pandas DataFrame:
#         import pandas as pd
#         import io
#         file_stream = io.StringIO(file.read().decode('utf-8'))
#         df = pd.read_csv(file_stream, delimiter=';')
#         results = ""
        
#         for i in range(len(df)):
        
#             input_values = [df["PRG"][i], df["PL"][i], df["PR"][i], df["SK"][i], df["TS"][i], df["M11"][i], df["BD2"][i], df["Age"][i], df["Insurance"][i]]
#             user_display = int(df["ID"][i])
#             prediction = model.predict([input_values])[0]
#             probabilities = model.predict_proba([input_values])[0]
#             probability = round(probabilities[prediction] * 100, 2) 
#             # Enregistrer la prédiction dans la base de données
#             new_prediction = Prediction(
#                 user_id=user_display,
#                 PRG=df["PRG"][i],
#                 PL=df["PL"][i],
#                 PR=df["PR"][i],
#                 SK=df["SK"][i],
#                 TS=df["TS"][i],
#                 M11=df["M11"][i],
#                 BD2=df["BD2"][i],
#                 Age=df["Age"][i],
#                 Insurance=df["Insurance"][i],
#                 prediction=prediction,
#                 probability=probability
#             )

#             db.session.add(new_prediction)
#             db.session.commit()
            
#             header = '''<!doctype html>
#             <html lang="en">
#             <head>
#                 <meta charset="utf-8">
#                 <title>Résultat de la prédiction</title>
#                 <link rel="stylesheet" href="{{ url_for('static', filename='css/style_result.css') }}">
#             </head>
#             <body>
#                 <h1>Résultat de la prédiction</h1>'''
            
#             footer = '''
#                 <a href="/medecin/upload">Retour</a>
#             </body>
#             </html>'''
            
#             results+=f'''<p>La prédiction du modèle pour le patient {user_display} est {prediction}, avec une probabilité associée de {probability}.<p>'''

#         return header + results + footer
    
#     else:
#         return '''
#         <!doctype html>
#         <html>
#         <head>
#         <title>Upload your data file</title>
#         </head>
#         <body>
#         <h1>Upload your data file</h1>
#         <form method=post enctype=multipart/form-data>
#           <input type=file name=file>
#           <input type=submit value=Upload>
#         </form>
#         </body>
#         </html>
#         '''

# ########################################################################################################################


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




# @app.route('/health')
# @login_required
# def health():
#     return render_template('user_input.html')

# @app.route('/health/predict', methods=['POST'])
# @login_required
# def predict():
#     PRG = float(request.form['PRG'])
#     PL = float(request.form['PL'])
#     PR = float(request.form['PR'])
#     SK = float(request.form['SK'])
#     TS = float(request.form['TS'])
#     M11 = float(request.form['M11'])
#     BD2 = float(request.form['BD2'])
#     Age = float(request.form['Age'])
#     Insurance = float(request.form['Insurance'])

#     input_values = [PRG, PL, PR, SK, TS, M11, BD2, Age, Insurance]

#     prediction = model.predict([input_values])[0]
#     probabilities = model.predict_proba([input_values])[0]
#     probability = round(probabilities[prediction] * 100, 2)

#     # Enregistrer la prédiction dans la base de données
#     new_prediction = Prediction(
#         user_id=current_user.id,
#         PRG=PRG,
#         PL=PL,
#         PR=PR,
#         SK=SK,
#         TS=TS,
#         M11=M11,
#         BD2=BD2,
#         Age=Age,
#         Insurance=Insurance,
#         prediction=prediction,
#         probability=probability
#     )

#     db.session.add(new_prediction)
#     db.session.commit()

#     return render_template('prediction_result.html', prediction=prediction, probability=probability)



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000,debug=True)