from email import message
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from helpers import test_Drinking, predict_WellType
import os

app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///files.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'profiles')


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":

        if request.form.get("button-start"):
            return redirect(url_for("load"))

    else:
        return render_template("index.html")


@app.route("/load" , methods = ["GET", "POST"])
def load():
    if request.method == "POST":

        if request.form.get("load"):

            uploaded_file = request.files.get("choose")

            if uploaded_file.filename != '':

                db.engine.execute("INSERT INTO profiles (filename) VALUES (?)", uploaded_file.filename)
                uploaded_file.save(os.path.join(UPLOAD_PATH, uploaded_file.filename))

                return redirect(url_for("predict"))
            
            return render_template("load.html")

    else:
        return render_template("load.html")


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        
        if request.form.get("predict"):
            rows = list(db.engine.execute("SELECT * FROM profiles"))
            
            if rows:
                filepath = os.path.join(UPLOAD_PATH, rows[0]['filename'])
                
                # add prediction with cheking any errors
                try:
                    drinking, well_type = "--", "--"

                    if request.form.get("drinking") and request.form.get("wellType"):
                        drinking = test_Drinking(filepath)
                        well_type = predict_WellType(filepath)

                    elif request.form.get("drinking"):
                        drinking = test_Drinking(filepath)
                    
                    elif request.form.get("wellType"):
                        well_type = predict_WellType(filepath)
                    
                    else:
                        drinking = test_Drinking(filepath)
                        well_type = predict_WellType(filepath)

                    return render_template("predict.html", drinking = drinking, well_type = well_type, predictinfo = "Diagnostics:")
                
                except:
                    return render_template("predict.html", predictinfo = "Invalid file")
                
                finally:
                    db.engine.execute("DELETE FROM profiles")
                    os.remove(filepath)
            
            else:
                return render_template("predict.html")
        
        elif request.form.get("new-evaluation"):
            return redirect(url_for("load"))

    else:
        return render_template("predict.html")
