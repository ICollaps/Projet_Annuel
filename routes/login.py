from flask import Blueprint, render_template , abort , redirect , request , flash , url_for , make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId



from utils.config import db
from utils.functions import is_db_up

login_bp = Blueprint('login_bp', __name__)

login_manager = LoginManager()


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
    if not is_db_up():
        raise Exception('Database error') 

    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return UserObj(user)


@login_bp.route('/login', methods=['GET', 'POST'])
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





@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté avec succès.', 'success')
    return redirect(url_for('login_bp.login'))







@login_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('login_bp.register'))
        
        

        if role == 'patient' :
            doctor_name = request.form.get('doctor_name_select')
            new_user = {'username': username, 'password': hashed_password, 'role': role , 'doctor_name' : doctor_name , 'email' :  email , 'first_name' : first_name , 'last_name' : last_name}
        elif role == 'médecin' :
            new_user = {'username': username, 'password': hashed_password, 'role': role , 'email' :  email , 'first_name' : first_name , 'last_name' : last_name}
        elif role == 'admin' :
            new_user = {'username': username, 'password': hashed_password, 'role': role}

        db.users.insert_one(new_user)
        flash("Inscription réussie ! Veuillez vous connecter.", 'success')
        return redirect(url_for('login_bp.login'))

    return render_template('register.html' , doctors=doctors)