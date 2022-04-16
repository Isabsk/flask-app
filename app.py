from flask import Flask,render_template,request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
   return 'hello guys'


@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

if __name__ == "__main__":
    app.run()


from flask import Flask,render_template,request
import psycopg2

app = Flask(__name__)

host = "ec2-34-192-210-139.compute-1.amazonaws.com"
database = "d2i7q91fs596j9"
user = "jtpeewohnbodnj"
password = "79665d383895d2e0213a880e3a57d3fe725cbd38b4ea9bf93fbee6f2b872e0bc"
port = "5432"

def initial():
   conn = get_db_connection()
   cur = conn.cursor()
   try:
      cur.execute("CREATE TABLE IF NOT EXISTS students (id serial PRIMARY KEY, name varchar (150) NOT NULL, addr varchar (50) NOT NULL, city varchar (50) NOT NULL, pin integer NOT NULL)")
      conn.commit()
      cur.close()
      conn.close()
      return
   except Exception as e:
      cur.close()
      conn.close()
      return
   cur.close()
   conn.close()
   return


def get_db_connection():
   try:
      conn = psycopg2.connect(
               host=host,
               database=database,
               user=user,
               password=password,
               port=port)
   except Exception as e:
      print(e)
      return None
   return conn


@app.route('/')
def home():
   return 'hello guys'


@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      msg = "Failed... "
      initial()
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         conn = get_db_connection()

         # Open a cursor to perform database operations
         cur = conn.cursor()
         try:
            cur.execute('INSERT INTO students (name,addr,city,pin)'
            'VALUES (%s, %s, %s, %s)',
            (nm,addr,city,pin))
         
            conn.commit()
            msg = "Record successfully added"
            cur.close()
            conn.close()
         except Exception as e:
            cur.close()
            conn.close()
      except:
         msg = "error in insert operation"
      
      finally:
         cur.close()
         conn.close()
         return render_template("result.html",msg = msg)
         

@app.route('/list')
def list():
   con = get_db_connection()
   
   cur = con.cursor()
   cur.execute("SELECT * FROM students;")
   
   rows = cur.fetchall(); 
   cur.close()
   con.close()
   return render_template("list.html",rows = rows)

if __name__ == "__main__":
   app.run()

