import sqlite3
from flask import Flask, request,jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS USERS (id integer primary key autoincrement,name TEXT, surname TEXT, email TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/register_user/', methods=['POST','GET'])
def register_user():
    msg = None
    if request.method == "POST":
        try:
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute("INSERT INTO USERS (name, surname, email, password) VALUES (?, ?, ?, ?)", (name, surname, email, password))
                con.commit()
                msg = "Record successfully added."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)


@app.route('/show-records/', methods=["GET"])
def show_records():
    data = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM USERS")
            data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database." + str(e) )
    finally:
        con.close()
        return jsonify(data)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = None
    email = request.form['email']
    password = request.form['password']
    if password == ['password']:
        try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute('SELECT * FROM USERS WHERE email = ? and password = ?', (email, password))
                con.commit()
                msg = email + " has logged in."
        except Exception as e:
            con.rollback()
            msg = "There was a problem logging in try again later " + str(e)
        finally:
            con.close()
        return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)

