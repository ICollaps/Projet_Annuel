from pymongo import MongoClient
import joblib



client = MongoClient('mongodb://localhost:27017/Annual_Project' )
# client = MongoClient('mongodb://host:27017/')
db = client['Annual_Project']
# db = client.get_default_database()


model = joblib.load("model/trained_models/best_model.pkl")
