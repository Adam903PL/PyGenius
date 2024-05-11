from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def login():
    return render_template('admin.html')



@app.route('/login_data',methods=['POST'])
def login_data():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with open("logs.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")

        
        return f'Login attempt with username: {username} and password: {password}'

if __name__ == '__main__':
    app.run(debug=True)
