from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

import pandas as pd
import pyodbc

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-LVMILT8\SQLEXPRESS;'
                      'Database=sandbox;'
                      'Trusted_Connection=yes;')
conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
conn.setencoding('latin1')
mycursor = conn.cursor()

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        print(file_path)
        parseCSV(file_path)
        # save the file
    return redirect(url_for('index'))

def parseCSV(filePath):
    # Loop through the Rows
    if filePath == 'static/files\jobs.csv':
        # CVS Column Names
        col_names = ['id','job']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath,names=col_names, header=None)
        for row in csvData.itertuples():
            mycursor.execute('''
                        INSERT INTO jobs (id, job)
                        VALUES (?,?)
                        ''',
                        row.id, 
                        row.job
                        )
        conn.commit()
    elif filePath == 'static/files\departments.csv':
        # CVS Column Names
        col_names = ['id','department']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath,names=col_names, header=None)
        for row in csvData.itertuples():
            mycursor.execute('''
                        INSERT INTO departments (id, department)
                        VALUES (?,?)
                        ''',
                        row.id, 
                        row.department
                        )
        conn.commit()
    else:
        #filePath == 'static/files\hired_employees.csv':
        # CVS Column Names
        col_names = ['id','name','datetime','department_id','job_id']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath,names=col_names, header=None)
        
        csvData[['department_id','job_id']] = csvData[['department_id','job_id']].fillna(0)
        csvData[['department_id','job_id']] = csvData[['department_id','job_id']].astype(int)
        csvData[['name','datetime']] = csvData[['name','datetime']].fillna('')
        csvData[['name','datetime']] = csvData[['name','datetime']].fillna(str)
        for row in csvData.itertuples():
            mycursor.execute('''
                        INSERT INTO hired_employees (id, name, datetime, department_id, job_id)
                        VALUES (?,?,?,?,?)
                        ''',
                        row.id,
                        row.name,
                        row.datetime,
                        row.department_id,
                        row.job_id
                        )
        conn.commit()

if (__name__ == "__main__"):
     app.run(port = 5000)
