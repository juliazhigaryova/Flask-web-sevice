from flask import Flask, request, jsonify,abort,redirect, url_for,render_template,send_file
from joblib import dump, load
import numpy as np
import pandas as pd

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
        filename = form.name.data + '.csv'
        # f.save(os.path.join(
        #     filename
        # ))

        df = pd.read_csv(f, header=None)
        pred = knn.predict(df)
        result = pd.DataFrame(pred)
        result.to_csv(filename,index=False)

        return send_file(filename,
                         mimetipe='text/csv',
                         attachment_filename=filename,
                         as_attachment=True)

    return render_template('submit.html', form=form)

    import os
    from flask import Flask, flash, request, redirect, url_for
    from werkzeug.utils import secure_filename
    from werkzeug.utils import safe_str_cmp

    UPLOAD_FOLDER = ''
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename + 'uploaded')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return 'file uploaded'
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

