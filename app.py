import sqlite3
import os
from flask import Flask , render_template , make_response , request , session , redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "2af888e0942c476c4eaeab2880a9e3d3a1426acb86730c1bd60b6d339f2256b2"


@app.route("/main",  methods = ['GET' , 'POST'])
def base():
    if request.method == 'GET':
        return render_template('main.html')

@app.route("/auth" , methods = ['GET' , 'POST'])
def index():
    if request.method == 'GET':
        if 'auth' in session and session['auth']:
            response = make_response(redirect(f"/main"))
            return response
            
        else:
            return render_template('auth.html')
    else:
        mail = request.form.get('login')
        password = request.form.get('pass')

        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"SELECT * FROM Users WHERE Mail = '{mail}' "
            result = cur.execute(sql).fetchone()
            print(result)
            if (result and result[3] == password):

                session['login'] = result[2]
                session['id'] = result[0]
                session['auth'] = True 
                response = make_response(redirect(f"/main"))
                return response
            else:
                return render_template('auth.html')
        return "123"


@app.route("/reg" ,  methods = ['GET' , 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')

    if request.method == 'POST':
        mail = request.form.get('mail')
        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"SELECT * FROM Users WHERE Mail = '{mail}'"
            print(sql)
            result = cur.execute(sql).fetchone()

        if result:
            return "Такой пользователь уже существует"

        login = request.form.get('login')
        password = request.form.get('password')

        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"""INSERT INTO Users ('Mail' , 'Login' , 'Password') 
            VALUES ('{mail}','{login}','{password}')"""
            cur.execute(sql)
            cur.commit()

        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"SELECT ID FROM Users WHERE Mail = '{mail}'"
            result = cur.execute(sql).fetchone()
        
        session['login'] = login
        session['id'] = result[0]
        session['auth'] = True

        response = make_response(redirect(f"/main"))
        return response

@app.route("/games/<id>", methods =['GET','POST'])
def game(id):
    print(id)

    with sqlite3.connect("jomgamestore.db")as cur:
        sql=f"SELECT * FROM games WHERE id = '{id}' "
        result = cur.execute(sql).fetchone()
        if(result):

            return render_template('index.html',data=result)


@app.route("/games/<id>/play")
def play(id):
    with sqlite3.connect("jomgamestore.db")as cur:
        sql=f"SELECT * FROM games WHERE id = '{id}' "
        result = cur.execute(sql).fetchone()
        if(result):
            return render_template(id+'/index.html')

@app.route("/gamelist", methods=['GET','POST'])
def gamelist():
    if request.method =='GET':
        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"SELECT * FROM games"
            games = cur.execute(sql).fetchall()
        
        print(games)
        return (render_template('search.html' , data = games))

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method =='GET':
        return (render_template('search.html'))
    if request.method =='POST':
        name = request.form.get('name')
        with sqlite3.connect("jomgamestore.db") as cur:
            sql = f"SELECT * FROM games WHERE name like '%{name}%'"
            games = cur.execute(sql).fetchall()
            if(games):
                print(games)
                return (render_template('search.html' , data = games))
app.run(debug=True)
'''пред-укзать в поле зпросаа'''