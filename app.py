import hashlib
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import psycopg2

app = Flask(__name__)
app.secret_key = 'Jakub Mazurek'
external_database_url = 'postgres://pygenius_security_db_user:2nUg1JYDa5Fgjw0lhOFfNt7ROpKkPSgO@dpg-cp1t92821fec738hjbk0-a.oregon-postgres.render.com/pygenius_security_db'




@app.route('/logout_user')
def logout_user():
    session.clear()
    return redirect(url_for('login'))




@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
             return redirect(url_for('admin_panel'))
    elif session:
        redirect(url_for('login'))
        return redirect(url_for('tasks'))
    return render_template('index.html')



@app.route('/help')
def help():
    return render_template('help.html')
    
@app.route('/login')
def login():
    if session:
        return redirect(url_for('tasks'))
    return render_template('login.html')



@app.route('/admin')
def register():
    return render_template('admin.html')

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








@app.route('/login/tasks')
def tasks():
    for key, value in session.items():
        if value is True:
            return render_template('tasks.html')
    return redirect(url_for('login'))
@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        connection = psycopg2.connect(external_database_url)
        cursor = connection.cursor()

        query = """
        SELECT  U.FirstName
        FROM LoginCredits AS LC
        JOIN Users AS U ON LC.UserId = U.UserId WHERE LC.Email = %s AND LC.Passwords = %s """
        cursor.execute(query, (email, password))

        row = cursor.fetchone()

        if row:
            with open("logs.txt", "a") as file:
                file.write(f"AAA ZALOGOWANO plik PyGenius \n")

            first_name = row[0]

            session[f'logged_in_{first_name}'] = True
            if session[f'logged_in_{first_name}'] == True:
                with open("logs.txt","a") as file:
                    file.write('Sesja dziala byqu \n')


            return f'Tak'

        else:
            with open("logs.txt", "a") as file:
                file.write(f"Login failed: Username: {email}, Password: {password}\n")
            return "Login failed: Incorrect email or password"

    except psycopg2.Error as ex:
        print(f'Błąd połączenia z bazą danych: {ex}')
        return "Database connection error"
    finally:
        if connection:
            cursor.close()
            connection.close()



@app.route('/getTasks', methods=['POST'])
def getTask():
    try:
        connection = psycopg2.connect(external_database_url)
        cursor = connection.cursor()

        query = """select TaskId,TaskName, HardLevel, Points, InputData, OutPutData, Description 
                   from TaskHeader
                   order by HardLevel asc"""
        cursor.execute(query)

        tasks_data = []  
        for row in cursor.fetchall():
            task_info = {
                'TaskId': row[0],
                'TaskName': row[1],
                'HardLevel': row[2],
                'Points': row[3],
                'InputData': row[4],
                'OutputData': row[5],
                'Description': row[6]
            }
            tasks_data.append(task_info)  

    except psycopg2.Error as ex:
        print(f'Błąd połączenia z bazą danych: {ex}')
        return jsonify({'error': 'Database connection error'})
    finally:
        if connection:
            cursor.close()
            connection.close()
        return jsonify({'tasks': tasks_data})  

try:
    dane = getTask()
    with open("logs.txt", "a") as file:
        file.write(f"Dane: {dane}\n")
except Exception as e:
    print(f"An error occurrfed: {e}")


if __name__ == '__main__':
    app.run(debug=True)