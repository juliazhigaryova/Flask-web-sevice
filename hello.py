from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    print('Hey there!')
    return "<h1>Hello, my friend!</h1>"

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

if __name__ == '__main__':
   app.run(host='0.0.0.0')