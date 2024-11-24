# Importing required modules
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import requests
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

# Import the database instance
from db_instance import db

# Immigration Checkpoint Workflow Logic
from immigration_logic import immigration_walkthrough

# Import mock_data function
from mock_data import insert_mock_data

# Initializing Flask App
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads' # Directory where uploaded images will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Use Upload_Folder for file uploads
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immigration.db' # SQLite Database URI for local testing
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
TOKEN = "210ed0449ee06e8d9bcee4a67c742814e4e7366e" # This is the PlateRecognizer API Token
API_URL = "https://api.platerecognizer.com/v1/plate-reader/" # This is the PlateRecognizer API Url


# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize SQLAlchemy for the Flask app
db.init_app(app)


# Defines the route for Homepage (consisting of Image Upload)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    # POST Method is called
    if request.method == 'POST':

        # If no file uploaded, reload current page
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the filename is empty, reload current page 
        if file.filename == '':
            return redirect(request.url)
        
        # If file was correctly uploaded so far
        if file:

            # Sanitize the filename
            filename = secure_filename(file.filename)

            # Save uploaded file to specific path/folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the image using PlateRecognizer API
            license_plate = recognize_license_plate(file_path, TOKEN)

            if "Error" in license_plate or license_plate == "No license plate detected.":
                return render_template('upload.html', filename=filename, license_plate=license_plate)
            
            # Start the database logic process
            immigration_result = immigration_walkthrough(license_plate)
            
            return render_template('upload.html', filename=filename, license_plate=license_plate, immigration_result=immigration_result)

    
    # GET Method is called
    else:
        return render_template('upload.html')

# Function to recognize license plate using PlateRecognizer API
def recognize_license_plate(image_path, token):

    # Create headers dictionary for authentication
    headers = {
        "Authorization": f"Token {token}"
    }

    with open(image_path, "rb") as fp:

        # Send request to Plate Recognizer
        response = requests.post(API_URL, headers=headers, files={"upload": fp})
        
        # If request was successful
        if response.status_code == 200 or response.status_code == 201:
            
            data = response.json()
            if data['results']:
                
                # Extract license plate from the response
                return data['results'][0]['plate']
            
            else:
                return "No license plate detected."
        
        else:
            return f"Error: {response.status_code}, {response.text}"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':

    with app.app_context():

        # Drop all tables to start fresh
        db.drop_all()

        # Create database tables
        db.create_all() 

        # Insert mock data
        insert_mock_data()  

    app.run(debug=True)
