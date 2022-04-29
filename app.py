











 





         
        
        
         
         
       
         
         
            
           
            
   
    
    
      

   






   


   







from flask import Flask,render_template,request
import psycopg2

app = Flask(__name__)

host = "ec2-3-217-251-77.compute-1.amazonaws.com"
database = "dfte8kcocghqd1"
user = "jvpfbupfprpppg"
password = "1962dbcac2400621ee34a21b2d193ff8de8dfc82f600c81daa67ba4c1d0a50ed"
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

