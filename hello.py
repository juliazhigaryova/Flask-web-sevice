from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    print('Hey there!')
    return "<h1>Hello, my friend!</h1>"