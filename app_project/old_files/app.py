from flask import Flask, render_template

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config['SECRET_KEY']= '123'

class fileUploader(FlaskForm):
    file= FileField("File")
    submit=SubmitField("Upload File")


ui = FlaskUI(app, width=500, height=500)

@app.route("/",methods=["POST","GET"])
@app.route("/home",methods=["POST","GET"])
def home():
    form = fileUploader()
    return render_template("index.html",form=form)

if __name__ == "__main__":
    ##app.run()
    ui.run()