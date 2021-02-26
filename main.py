import sqlite3
from flask import Flask, request,jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, surname TEXT, email TEXT, password TEXT)')
    print("Table for users created successfully")
    conn.close()

init_sqlite_db()


def products_table():
    conn1 = sqlite3.connect('database.db')
    conn1.execute('CREATE TABLE IF NOT EXISTS PRODUCTS (ID INTEGER PRIMARY KEY AUTOINCREMENT, cellphone_names TEXT NOT NULL, prices TEXT NOT NULL, images BLOP NOT NULL)')
    print("Table for products created")
    conn1.close()


products_table()


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


@app.route('/products/')
def insert_products():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('0','Samsung Galaxy S5', 'R3999', 'https://i.postimg.cc/KzdGbNVp/mobile-1843328-1920.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('1','MI Xiamoah', 'R5999', 'https://i.postimg.cc/7YX8nRjp/1576.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('2','Hisence X3', 'R3999', 'https://i.postimg.cc/KzdGbNVp/mobile-1843328-1920.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('3','Apple Iphone 7', 'R7999', 'https://i.postimg.cc/5Nf6s62j/59949.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('4','Hauwei P9 Lite', 'R8950', 'https://i.postimg.cc/3xT5Xv8b/89354.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('5','P6YUM70', 'R12999','https://i.postimg.cc/Jz23wbsp/P6YUM70.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('6','Neo AI', 'R5999', 'https://i.postimg.cc/sgmj1cYJ/neonbrand-z3k-BG5x-Ihjo-unsplash.jpg')")
            cur.execute("INSERT INTO PRODUCTS(ID,cellphone_names,prices,images) VALUES('7','Apple Ipad', 'R13999', 'https://i.postimg.cc/B6LPxyN3/board-1362851-1280.png')")
            con.commit()
            msg = "Record successfully added."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)

