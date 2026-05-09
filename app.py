from flask import Flask, render_template, jsonify, request
from entities.categorias import Categorias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
