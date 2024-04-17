from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

MONGO_URI = 'mongodb+srv://cduong:Hungyeuem2001@cluster0.gu7twaw.mongodb.net/'
db_name = "Project"
client = MongoClient(MONGO_URI)
db = client[db_name]
riskPrediction = db.mydata  
if __name__ == '__main__':
    app.run(debug=True)