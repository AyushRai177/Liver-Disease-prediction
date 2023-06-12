from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database_setup import opendb, DB_URL
from database_setup import User, Profile
from db_helper import *
from validators import *
from werkzeug.utils import secure_filename
import os
import pandas as pd
import joblib
import datetime

app = Flask(__name__)

app.secret_key = 'my-secret-key' 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_2():
    return render_template('home.html')

@app.route('/why_random_forest')
def random():
    return render_template('why random.html')

@app.route('/processed_data')
def process():
    return render_template('processed data.html')

@app.route('/form', methods=['POST','GET'])
def show_form():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        tbil=request.form.get('tbil')
        dbil=request.form.get('dbil')
        alkphos=request.form.get('alkphos')
        sgpt=request.form.get('sgpt')
        sgot=request.form.get('sgot')
        tp=request.form.get('tp')
        alb=request.form.get('alb')
        agr=request.form.get('agr')
        

        session['name'] =name
        session['age']=age
        session['gender']=gender
        session['tbil']=tbil
        session['dbil']=dbil
        session['alkphos']=alkphos
        session['sgpt']=sgpt
        session['sgot']=sgot
        session['tp']=tp
        session['alb']=alb
        session['agr']=agr

        input_df = create_df(age, gender, tbil, dbil, alkphos, sgpt, sgot, tp, alb, agr) 
        prediction = predict(input_df)[0]
        session['prediction']=int(float(prediction))
        print(session['prediction'])
        return render_template('result.html',input_df=input_df.to_html(), prediction=prediction)

    return render_template('form.html')

def create_df(age, gender, tbil, dbil, alkphos, sgpt, sgot, tp, alb, agr):
    df = pd.DataFrame({
        'Age of the patient': [age],
        'Gender of the patient': [gender],
        'Total Bilirubin': [tbil],
        'Direct Bilirubin': [dbil],
        'Alkphos Alkaline Phosphotase': [alkphos],
        'Sgpt Alamine Aminotransferase': [sgpt],
        'Sgot Aspartate Aminotransferase': [sgot],  
        'Total Protiens': [tp],
        'ALB Albumin': [alb],
        'A/G Ratio Albumin and Globulin Ratio': [agr]
    })

    print(df.loc[0])
    return df

def predict(data_df):
    # Load the trained model and scaler
    model = joblib.load(r'C:\Users\Ayush Rai\Downloads\final (3)\final\your_model.pkl')
    scaler = joblib.load(r'C:\Users\Ayush Rai\Downloads\final (3)\final\your_scaler.pkl')

    # Scale the input data using the scaler
    # scaled_data = scaler.transform(data_df)

    # Make predictions using the trained model
    predictions = model.predict(data_df)
    return predictions

@app.route('/report')
def show_report():
    name = session.get('name')  # Retrieve the variable_name from session
    age=session.get('age')
    gender=session.get('gender')
    tbil=session.get('tbil')
    dbil=session.get('dbil')
    alkphos=session.get('alkphos')
    sgpt=session.get('sgpt')
    sgot=session.get('sgot')
    tp=session.get('tp')
    alb=session.get('alb')
    agr=session.get('agr')
    prediction=session.get('prediction')
    report_date = date()    
    return render_template('report.html', name=name,age=age,gender=gender,tbil=tbil,dbil=dbil,
                           alkphos=alkphos,sgpt=sgpt,sgot=sgot,tp=tp,alb=alb,agr=agr,
                           prediction=prediction, report_date=report_date)
def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/signup', methods=['POST','GET'])
def signup():
    return render_template('signup.html')

@app.route('/what_is_liver_disease')
def what_is_liver_disease():
    return render_template('what is liver disease.html')

@app.route('/How_diet_can_affect_liver_health')
def How_diet_can_affect_liver_health():
    return render_template('How diet can affect liver health.html')

@app.route('/Liver_disease_in_children_what_parents_should_know')
def Liver_disease_in_children_what_parents_should_know():
    return render_template('Liver disease in children what parents should know.html')

@app.route('/New_study_finds_link_between_alcohol_consumption_and_liver_disease')
def New_study_finds_link_between_alcohol_consumption_and_liver_disease():
    return render_template('New study finds link between alcohol consumption and liver disease.html')

@app.route('/about_attributes')
def attribute():
    return render_template('About attributes.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
