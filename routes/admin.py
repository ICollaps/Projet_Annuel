from flask import Blueprint, render_template , abort , redirect , request , flash , url_for , make_response
from flask_login import login_required , current_user
from bson import ObjectId
from functools import wraps

from utils.config import db



admin_bp = Blueprint('admin_bp', __name__)



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function




@admin_bp.route('/admin')
@login_required
@admin_required
def admin():

    

    my_id = current_user.id

    users = db.users.find({"_id": {"$ne": ObjectId(my_id)}})
    predictions = db.predictions.find()
    return render_template('admin.html', users=users , predictions=predictions)




@admin_bp.route('/delete_users', methods=['POST'])
@login_required
@admin_required  # Make sure only admin can delete users
def delete_users():
    # Getting the list of user IDs from the form
    user_ids = request.form.getlist('user_ids')
    print(user_ids)
    # Deleting the users by their _id
    for user_id in user_ids:
        # Ensure the user_id is not an empty string
        if user_id:
            db.users.delete_one({"_id": ObjectId(user_id)})
    
    flash(f"{len(user_ids)} utilisateur(s) ont été supprimé(s) avec succès.", "success")
    return redirect(url_for('admin_bp.admin'))




@admin_bp.route('/delete_predictions', methods=['POST'])
@login_required
@admin_required  # Make sure only admin can delete predictions
def delete_predictions():
    # Getting the list of prediction IDs from the form
    prediction_ids = request.form.getlist('prediction_ids')

    print(prediction_ids)
    # Deleting the predictions by their _id
    for prediction_id in prediction_ids:
        db.predictions.delete_one({"_id": ObjectId(prediction_id)})

    flash(f"{len(prediction_ids)} prédiction(s) ont été supprimée(s) avec succès.", "success")
    return redirect(url_for('admin_bp.admin'))