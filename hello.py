from flask import Flask, request, jsonify,abort,redirect, url_for,render_template
from joblib import dump, load
import numpy as np

app = Flask(__name__)
knn = load('knn.pkl')

@app.route("/")
def hello_world():
    print('Hey there!')
    return "<h1>Hello, friend!</h1>"

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

if __name__ == '__main__':
   app.run(host='0.0.0.0')


@app.route('/iris/<param>')
def iris(param):
    pred = predict(param)
    iris_class = {1: 'setosa', 2: 'versicolor', 3: 'virginica'}
    name_class = iris_class.get(int(pred))
    return show_image(name_class)

@app.route('/show_image')
def show_image(name):
    return '<img src="/static/' + name +'.jpg" alt="IRIS flower">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)

@app.route('/iris_post', methods=['POST'])
def add_message():

    try:
        content = request.get_json()
        pred_val = predict(content["flower"])
        pred = {'class': str(pred_val[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(pred)

def predict(param):
    param = param.split(',')
    param = [float(num) for num in param]
    param = np.array(param).reshape(1, -1)
    return knn.predict(param)

from flask_wtf import FlaskForm
from wtforms import StringField,FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csfr secret key"
))

class MyForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = form.name.data + '.txt'
        f.save(os.path.join(
            filename
        ))
        return (str(form.name))

    return render_template('submit.html', form=form)

