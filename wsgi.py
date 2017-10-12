from flask import Flask, render_template, flash, request,send_from_directory
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import GenderClassifier
import os, random
from PIL import Image
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
predicted_gender=None
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route('/upload/<filename>')
def send_image(filename):
    if predicted_gender=="Boy":
        return send_from_directory("images/boy", filename)
    else:
        return send_from_directory("images/girl",filename)

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        print (name)
        g = GenderClassifier
        global predicted_gender
        predicted_name,predicted_gender = g.GenderClassifier.predict(name)
        if form.validate():
            # Save the comment here.
            flash('Predicted Gender : ' + predicted_gender)
            ran_boy = random.choice([x for x in os.listdir("images/boy")
                               if os.path.isfile(os.path.join("images/boy", x))])
            #ran_boy=os.path.join(folder_boy,ran_boy)
            ran_girl=random.choice([x for x in os.listdir("images/girl")
                               if os.path.isfile(os.path.join("images/girl", x))])
            #ran_girl=os.path.join(folder_girl,ran_girl)
            if(predicted_gender=="Boy"):
                return render_template('hello.html',form=form,image_names=[ran_boy])
            else:
                return render_template('hello.html',form=form,image_names=[ran_girl])
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('hello.html',form=form)

if __name__ == "__main__":
    app.run(threaded=True)
