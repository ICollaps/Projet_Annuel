from flask import Flask, redirect, url_for, render_template , request , flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from functools import wraps
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

app.config['LOGIN_VIEW'] = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'some_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ROLE_CHOICES = [('patient', 'Patient'), ('médecin', 'Médecin'), ('admin', 'Admin')]
    role = db.Column(db.String(10), nullable=False, default='patient')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Vous êtes connecté avec succès !', 'success')
            if user.role == 'admin':
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
        role = request.form['role']  # Ajoutez cette ligne
        hashed_password = generate_password_hash(password, method='sha256')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Nom d'utilisateur déjà pris, veuillez en choisir un autre.", 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password, role=role)  # Modifiez cette ligne
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie ! Veuillez vous connecter.", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)




@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("L'utilisateur a été supprimé avec succès.", "success")
    return redirect(url_for('view_users'))





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

    return render_template('prediction_result.html', prediction=prediction, probability=probability)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)