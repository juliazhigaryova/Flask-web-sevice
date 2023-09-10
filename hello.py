from flask import Flask
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
    param = param.split(',')
    param = [float(num) for num in param]
    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param)
    iris_class = {1: 'setosa', 2: 'versicolor', 3: 'virginica'}
    name_class = iris_class.get(int(predict))
    return show_image(name_class)

@app.route('/show_image')
def show_image(name):
    return '<img src="/static/' + name +'.jpg" alt="IRIS flower">'