Heart Attack Risk Prediction Web App

This web application is designed to predict the risk of heart attacks based on various health indicators and patient history. Utilizing MongoDB for data storage, the app integrates predictive analytics with user data management, offering both data insertion and risk prediction functionalities.

<img width="1253" alt="Screenshot 2024-04-05 at 11 26 03 PM" src="https://github.com/ogulewefortune/Heartattackanalysis/assets/74354924/62d8fec0-6568-4078-857c-a1bd444044fe">

Features

Data Insertion: Users can input personal health data, including age, cholesterol levels, heart rate, diabetes status, and more.
Risk Prediction: Based on inserted data, the app predicts the risk of a heart attack using a machine learning model.
Data Search: Users can search the database for patient records based on specific criteria such as age, sex, and health conditions.
Tech Stack

Frontend: HTML, CSS
Backend: Python (Flask)
Database: MongoDB
Machine Learning Model: Scikit-learn (Python)
File Structure

main.py: The Flask application's entry point. It defines routes and integrates all components.
prediction.py: Contains the logic for predicting heart attack risk using input data.
graphs.py: Utility file for generating and managing graphical representations of data (if applicable).
connection.py: Manages the MongoDB connection and data transactions.
predict.html, insert-record.html, search.html: HTML templates for the application's web interface.
Setup Instructions

Install Dependencies:
Ensure Python 3 and pip are installed on your system. Install the required Python packages using:
pip install flask pymongo scikit-learn
atabase Configuration:
Ensure MongoDB is installed and running on your system. Update connection.py with your MongoDB connection details.
Run the Application:
Execute the following command in the terminal:
python main.py

This will start the Flask server. Access the web application by navigating to http://localhost:5000 in your web browser.
Using the Application:
To insert new patient records, navigate to the Insert Data page via the home page.
To predict heart attack risk, fill in the required health indicators on the Predict Data page.
To search for existing records, use the search functionality on the Search Data page.
