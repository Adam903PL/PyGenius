from flask import *
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'Jakub Mazurek'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def login():
    return render_template('admin.html')

@app.route('/login')
def login_user():
    return render_template('login.html')

@app.route('/templates')
def templates():
    folder_path = 'PyGenius/static'
    files = os.listdir(folder_path)
    with open("logs.txt", "a") as file:
        file.write(f"{files},msmsms\n")
    return render_template('template.html', files=files)



@app.route('/login_data', methods=['POST'])
def login_data():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        word = "admin"

        hash_md5 = hashlib.md5()
        hash_md5.update(word.encode())
        hashed_word = hash_md5.hexdigest()

        if username == 'admin' and password == hashed_word:
            session['logged_in'] = True

            with open("logs.txt", "a") as file:
                file.write(f"Zalogowano Username: {username}, Password: {password}\n")

            redirect(url_for('admin_panel'))
            return f'Tak' 
        else:
            # Logowanie nieudanego zdarzenia
            with open("logs.txt", "a") as file:
                file.write(f"Blad w logowaniu \n")

            return redirect(url_for('index'))


@app.route('/admin_panel')
def admin_panel():
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin_panel.html')  
    else:
        return redirect(url_for('login'))  


@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login'))  


if __name__ == '__main__':
    app.run(debug=True)