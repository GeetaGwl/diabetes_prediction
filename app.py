from flask import Flask,render_template,request,redirect,session
import mysql.connector
app=Flask(__name__,template_folder="templates")
import pickle
import numpy as np

app.secret_key="diabetes"
model = pickle.load(open("diabetes-prediction-logreg-model.pkl","rb"))


# Default HomePage -----
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Research")
def research():
    return render_template("research.html")

@app.route("/ContactUs")
def contact():
    return render_template("contact.html")

@app.route("/feed")
def feed():
    if session['logged_in']==False:
        return redirect('/Login')
    

    # render the age template
    return render_template('feed.html')

@app.route("/Login")
def login():
    return render_template("login.html")

# Login Page Starts -----------------------------------------------------------

@app.route("/log",methods=["post"])
def log():

    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='project_diabetic')
    cur=conn.cursor()
    
    email=str(request.form["myemail"])
    passw=str(request.form["mypassword"])
    
    cur.execute("select * from register_table where Email = '"+email+"' and Password = '"+passw+"' ")
    if(cur.fetchone()):
        session['logged_in'] = True
        session["username"]=email
        print("Login Sucessfully")
        return redirect("/Diagnosis")
        # return "login succesfully !"
    else:
        print("Please login with correct credentials")
        return redirect("/Login")
        # return "pls check err "
    
# Login Page Ends-----------------------------------------------------------------

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect('/')
@app.route("/Register")
def register():
    return render_template("registration.html")

### Register Page Code Starts----------------------------------------------------------------

@app.route("/save",methods=["post"])
def saved():

    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='project_diabetic')
    cur=conn.cursor()

    
    user=str(request.form["userName"])
    email=str(request.form["userEmail"])
    phone=str(request.form["userContact"])
    passw=str(request.form["userPassword"])
    
    cur.execute("insert into register_table (Name,Email,Contact,Password) values ('"+user+"','"+email+"','"+phone+"','"+passw+"')")
    conn.commit()
    return redirect("/Login")

# Register Page Code Ends-----------------------------------------------------------------

@app.route("/Diagnosis")
def diagnosis():
    if session["logged_in"]==False:
        return redirect('/Login')
    

    return render_template("diagnosis.html")    


# Diagnosis/Prediction part starts -----

@app.route("/predict", methods=['POST'])
def predict():
    Pregnancies = request.form['Pregnancies']
    Glucose = request.form['Glucose']
    BloodPressure = request.form['BloodPressure']
    BMI = request.form['BMI']
    DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
    Age = request.form['Age']

    Pregnancies= int(Pregnancies)
    Glucose= int(Glucose)
    BloodPressure = int(BloodPressure)
    BMI = float(BMI)
    DiabetesPedigreeFunction = float(DiabetesPedigreeFunction)
    Age = int(Age)

    final_features = np.array([(Pregnancies, Glucose, BloodPressure, BMI, DiabetesPedigreeFunction, Age)])
    prediction = model.predict(final_features)
    return render_template('Result.html', pred = prediction)



    #return render_template("diagnosis.html")


# Diagnosis/Prediction part Ends ------

if __name__ == '__main__':
    app.run(debug=True,port=2222)



    
