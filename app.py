from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sq


app = Flask(__name__)
DB_PATH = "users.db"


def get_db():
    conn = sq.connect(DB_PATH)
    conn.row_factory = sq.Row
    return conn

def start_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if request.method == 'POST':
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        if not username and not password:
            msg = "preencha Usuario e senha" 
        else: 
            db = get_db()
            cur = db.execute("SELECT *  FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            db.close()
            if user and user ['passowrd'] == password:
                return render_template("admin.html",username=username)
            else:
                mgs = "Usuário ou senha inválidos."
    return render_template("login.html", mgs=mgs)
            
if __name__=='__main__':
    start_db()
    app.run(debug=True)
