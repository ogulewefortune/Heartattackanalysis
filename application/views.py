from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymongo as pm
import pandas as pd
import matplotlib 
matplotlib.use('Agg')
from graphs import get_plot, scatter_plot
from prediction import setup_prediction_model,predictHeartRisk
from connection import db, riskPrediction
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint('views', __name__)

#login page
@views.route('/', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        # Login logic to check the user credential
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.users.find_one({"username": username})
        if user and user['password'] == password:
            return redirect(url_for('views.home_page'))  # Redirect to the main page after login
        else:
            # Else display error msg and render the login page 
            flash("Invalid credential")
            return redirect(url_for('views.login'))
     return render_template('login.html')
 
#signup page
@views.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
            # Get user info from the page
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirmPassword']
            
            # Signup logic
            if password == confirm_password:
            # Insert the new user into the database, if only the confirm pass matches with the pass
               db.users.insert_one({"username": username, "email": email, "password": password})
               return redirect(url_for('views.login'))
            else:  
                flash("Password doesn't match") # Display error message
                return redirect(url_for('views.signup')) # Render the signup page again
     return render_template('signup.html')
#home page
@views.route('/home')
def home_page():
    # Render the home page 
    return render_template('Index.html')

#preidction page
@views.route('/predict', methods=['POST', 'GET'])
def predict():
    result = None
    if request.method == 'POST':  
        # Convert "Yes" to 1 and "No" to 0 for relevant fields
        def convert_to_int(value):
            return 1 if value == "Yes" else 0
        # Convert Male and Female to 1 and 0
        def convert_sex_int(value):
            return 1 if value =="Male" else 0  
        # Create the user_input DataFrame from form data
        user_input = pd.DataFrame([{
                    'Age': int(request.form['age']),
                    'Cholesterol': int(request.form['cholesterol']),
                    'Heart Rate': int(request.form['heart_rate']),
                    'Diabetes': convert_to_int(request.form['diabetes']),  
                    'Family History': convert_to_int(request.form['family_history']),  
                    'Smoking': convert_to_int(request.form['smoking']), 
                    'Obesity': convert_to_int(request.form['obesity']),  
                    'Alcohol Consumption': convert_to_int(request.form['alcohol_consumption']),
                    'Exercise Hours Per Week': float(request.form['exercise_hours']),
                    'Previous Heart Problems': convert_to_int(request.form['previous_heart_problems']),  
                    'Medication Use': convert_to_int(request.form['medication_use']),  
                    'Stress Level': int(request.form['stress_level']),
                    'BMI': int(request.form['bmi']),
                    'Physical Activity Days Per Week': int(request.form['physical_activity_days']),
                    'Sleep Hours Per Day': int(request.form['sleep_hours']),
                    'Systolic_BP': int(request.form['systolic_bp']),
                    'Diastolic_BP': int(request.form['diastolic_bp']),
                    'Sex_Cat': convert_sex_int((request.form['sex'])),  # Handle as categorical
                    }])
        
        # Fetching data from database
        dataset = DataFrame(list(db.mydata.find()))
        dataset = dataset.drop(['_id'], axis=1)
        # Drop the target value
        targetCol = 'Heart Attack Risk'  
        y = dataset[targetCol]
        X = dataset.drop(targetCol, axis=1)
        # Prediction model
        predictionModel = setup_prediction_model(X,y)
        prediction = predictHeartRisk(user_input, predictionModel)
        
        # Determine the result based on the prediction 
        if prediction[0] == 1: 
            result = 'High risk of heart attack'
        else: 
            result = 'Low to No risk of heart attack'

    return render_template('predict.html', result=result if result is not None else '')


#insert records page
@views.route('/insert-record', methods = ['GET', 'POST'])
def insert_page():
    if request.method == 'POST':
        # Convert "Yes" to 1 and "No" to 0 for relevant fields
        def convert_to_int(value):
            return 1 if value == "Yes" else 0
        # Convert Male and Female to 1 and 0
        def convert_sex_int(value):
            return 1 if value =="Male" else 0
        # Get form data
        record = {
            "Patient ID": request.form['pid'],
            "Age": int(request.form['age']),
            "Sex": convert_sex_int((request.form['sex'])),
            "Cholesterol": int(request.form['cholesterol']),
            "Heart_rate": int(request.form['heart_rate']),
            "Diabetes": convert_to_int(request.form['diabetes']),
            "Family_history": convert_to_int(request.form['family_history']),
            "Smoking": convert_to_int(request.form['smoking']),
            "Obesity": convert_to_int(request.form['obesity']),
            "Alcohol_consumption": convert_to_int(request.form['alcohol_consumption']),
            "Exercise_hours": int(request.form['exercise_hours']),
            "Previous_heart_problems": convert_to_int(request.form['previous_heart_problems']),
            "Medication_use": convert_to_int(request.form['medication_use']),
            "Stress_level": convert_to_int(request.form['stress_level']),
            "Bmi": int(request.form['bmi']),
            "Physical_activity_days": int(request.form['physical_activity_days']),
            "Sleep_hours": int(request.form['sleep_hours']),
            "Systolic_bp": int(request.form['systolic_bp']),
            "Diastolic_bp": int(request.form['diastolic_bp']),
        }

        # Insert record into MongoDB heartAttackPrediction collection
        db.searchData.insert_one(record)

        return redirect(url_for('views.home_page'))
    else:
        return render_template('insert-record.html')

# Search page  
@views.route('/search', methods=['POST','GET'])
def search():
     if request.method == 'POST':
            # Convert "Yes" to 1 and "No" to 0 for relevant fields
            def convert_to_int(value):
                return 1 if value == "Yes" else 0
            # Convert Male and Female to 1 and 0
            def convert_sex_int(value):
                return 1 if value =="Male" else 0
            # Convert Male and Female to 1 and 0
            def convert_sort_int(value):
                return 1 if value == "Ascending" else -1 if value == "Descending" else None
            
            age_min = request.form.get('ageMin', type=int) or 0
            age_max = request.form.get('ageMax', type=int) or 120
            patient_id = request.form.get('pID')
            diabetes_status = convert_to_int(request.form.get('diabetes'))
            sex = convert_sex_int(request.form.get('sex'))
            obesity_status = convert_to_int(request.form.get('obesity'))
            sort_order = convert_sort_int(request.form.get('sort'))
                     
            # Constructing the base query
            query = {'$and': []}
        
            # Adding age filters
            if age_min or age_max:
                query['$and'].append({'Age': {'$gte': age_min}})
                query['$and'].append({'Age': {'$lte': age_max}})
        
            # Adding patient ID filter if provided
            if patient_id:
                query['$and'].append({'Patient ID': patient_id})

            if diabetes_status in ['1', '0']:
                query['$and'].append({'Diabetes': diabetes_status})
            
            if sex in ['1', '0']:
                query['$and'].append({'Sex': sex})
            
            if obesity_status in ['1', '0']:
                query['$and'].append({'Obesity': obesity_status})
                
                
            # If the user click on the sort by age option, then assign the sorting to query
            if sort_order is not None:
                results = list(db.searchData.find(query).sort('Age', sort_order))
            else:
                results = list(db.searchData.find(query))
                
            return render_template('search.html', rows=results)
        
     return render_template('search.html', rows=[])
   

#Visualize page
@views.route('/visualize', methods=['GET', 'POST'])
def visualize():
   # Queries the database to retrieve the required data
   # Queries the database to retrieve documents where 'Age','Sleep Hours Per Day', and Heart Rate is included
    data = db.heartAttackPrediction.find({
        '$and': [
            {'Age': {'$gt': 10}},  # Specify condition for 'Age' greater than 10
            {'Sleep Hours Per Day': {'$gt': 1}},  # Specify condition for 'Sleep Hours Per Day' greater than 4
            {'Heart Rate': {'$lt': 100}}  # Specify condition for 'Heart Rate' greater than 30
        ]
    }, {'_id': 0, 'Age': 1, 'Sleep Hours Per Day': 1, 'Heart Rate': 1})
    
    age_data = db.heartAttackPrediction.find({'Age': {'$gt': 10}}, {'Age': 1})
    

    # Convert the retrieved data to a pandas DataFrame
    dataset = pd.DataFrame(list(data))
    dataset_age = pd.DataFrame(list(age_data))
    
    #Chart for Age
    # Define parameters for the plot
    kind = 'bar'
    title = 'Age Distribution'
    xlabel = 'Age'
    ylabel = 'Number of People'
    sort = True
    limit = 20
    angle = 0  # Adjust the angle if needed

    # Generate plot using get_plot function from graphs.py
    age_plot = get_plot(dataset_age['Age'], kind, title, xlabel, ylabel, sort, limit, angle)

    #Chart for Sleep Hours
    # Define parameters for the sleep hours per day plot
    sleep_kind = 'bar'
    sleep_title = 'Sleep Hours Distribution'
    sleep_xlabel = 'Sleep Hours'
    sleep_ylabel = 'Number of People'
    sleep_sort = True
    sleep_limit = 10  # Adjust as needed
    sleep_angle = 0  # Adjust as needed

    # Generate plot for sleep hours distribution
    sleep_plot = get_plot(dataset['Sleep Hours Per Day'], sleep_kind, sleep_title, sleep_xlabel, sleep_ylabel, sleep_sort, sleep_limit, sleep_angle)

    #Chart for Age
    # Define parameters for the plot
    kind = 'bar'
    title = 'Heart Rate Distribution'
    xlabel = 'Heart Rate'
    ylabel = 'Number of People'
    sort = True
    heart_limit = 8
    angle = 0  # Adjust the angle if needed

    # Generate plot using get_plot function from graphs.py
    heart_plot = get_plot(dataset['Heart Rate'], kind, title, xlabel, ylabel, sort, heart_limit, angle)

    #query for all Stress Level and Sleep Hours Per Day not equal to 0
    data_scat = db.heartAttackPrediction.find({
    '$and': [
        {'Cholesterol': {'$lt': 200}},  # Specify condition for 'Stress Level' not equal to 0
        {'Heart Rate': {'$lt': 100}}  # Specify condition for 'Sleep Hours Per Day' not equal to 0
    ]
}, {'_id': 0, 'Cholesterol': 1, 'Heart Rate': 1})
    
    dataset_scat = pd.DataFrame(list(data_scat))

    #Chart for scatter
    fieldx = 'Cholesterol'
    fieldy = 'Heart Rate'
    title_scat = 'Chloesterol vs Heart Rate'
    xlabel_scat = 'Cholesterol'
    ylabel_scat = 'Heart Rate'

    scat_plot = scatter_plot(dataset_scat, fieldx, fieldy, title_scat, xlabel_scat, ylabel_scat)


    # Pass the base64-encoded image data to the template
    return render_template('visualize.html', age_plot=age_plot, sleep_plot=sleep_plot, heart_plot=heart_plot, scat_plot=scat_plot)
