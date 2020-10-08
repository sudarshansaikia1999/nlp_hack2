'''
A Web application that shows Google Maps around schools, using
the Flask framework, and the Google Maps API.
'''

from flask import Flask, render_template, abort,url_for,request
import pandas as pd
import pickle
import numpy as np
app = Flask(__name__)



model=pickle.load(open('model.pkl','rb'))



@app.route("/")
def index():
    return render_template('index.html')

###data set doesn't contain my country details. so taking an arbitary location for demo
@app.route("/visualization")
def vis():
    data= pd.read_csv("1_county_level_confirmed_cases.csv")


    loc=(data[data['lat']==34.69847452].index.values)
    population=data['total_population'][loc[0]]
    confirmed=data['confirmed'][loc[0]]
    deaths=data['deaths'][loc[0]]
    if (confirmed>=1000):
        text='Your symptoms are sevre! Consult doctors as early as possible '
        return render_template('visual.html',population=population,confirmed=confirmed,deaths=deaths,text=text)
    else:
        text= 'Low covid sensitive area!'
        return render_template('visual.html',pupulation=population,confirmed=confirmed,deaths=deaths,text=text)


@app.route("/health-check")
def check():
    return render_template('check.html')


@app.route('/health-check-up',methods=['GET','POST'])
def Disease():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    if output==0:
        prediction_text='Congratulations! You are completely fit'
    elif output==1:
        prediction_text='Severe Chance of covid19. consult doctor'
    return render_template('<h1>{{ prediction_text }}</h1>', prediction_text=prediction_text)



#for testing
'''
@app.route('/health-check-results')
def Pred():
    c=model.predict([[1,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,0]])
    d=c[0]
    return render_template('results.html')

'''
app.run(host='localhost', debug=True)