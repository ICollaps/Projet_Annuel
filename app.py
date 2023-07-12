from flask import Flask, render_template
from flask_login import login_required, current_user


from routes.medecin import medecin_bp
from routes.patient import patient_bp
from routes.admin import admin_bp
from routes.login import login_bp , login_manager



app = Flask(__name__)


app.register_blueprint(medecin_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)

# app.config['LOGIN_VIEW'] = 'login'

app.config['SECRET_KEY'] = 'some_secret_key'


login_manager.init_app(app)
login_manager.login_view = 'login'


    

@app.route('/')
def index():
    return render_template('welcome.html')




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
    




if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000,debug=True)