from flask import Flask,render_template,request,url_for,redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

Bootstrap(app)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html',place="home")

@app.route('/pay', methods=['GET','POST'])
def pay():
    if request.method == 'POST':
        if request.form.get('account') and  request.form.get('name') and not  request.form.get('amount') == '':
            print("send amount")
            form = request.form
            amount = form['amount']
            name = form['name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO transactions(name,amount) VALUES(%s,%s)",(name,amount))
            mysql.connection.commit()
            return render_template('pay.html',place="pay",send="yes")

        if request.form.get('account') and not request.form.get('name') and not  request.form.get('amount') == '':
            print("name is missing")
            acc=request.form.get('account')
            amt=request.form.get('amount')
            return render_template('pay.html',place="pay",send="name",account=acc,amount=amt)

        if not request.form.get('account') and request.form.get('name') and not  request.form.get('amount') == '':
            print("account no. is missing")
            name=request.form.get('name')
            amt=request.form.get('amount')
            return render_template('pay.html',place="pay",send="account",name=name,amount=amt)   

        if request.form.get('account') and not request.form.get('name') and request.form.get('amount') == '':
            print("details are not given")
            acc=request.form.get('account')
            return render_template('pay.html',place="pay",send="no",account=acc)
        
        if not request.form.get('account') and request.form.get('name') and request.form.get('amount') == '':
            print("details are not given")
            name=request.form.get('name')
            return render_template('pay.html',place="pay",send="no",name=name)
        
        if request.form.get("amount") == "" and not request.form.get('account') and not request.form.get('name'):
            print("none")
            return render_template('pay.html',place="pay",send="no")
        
        if request.form.get("amount") == "":
            print("none")
            return render_template('pay.html',place="pay",send="no")
    return render_template('pay.html',place="pay")

@app.route('/customers', methods=['GET','POST'])
def customers():
    cur = mysql.connection.cursor()  
    cur.execute("SELECT * FROM customers")
    data_list=cur.fetchall()
    return render_template('customers.html',place="customer",customers=data_list)

@app.route('/transactions', methods=['GET','POST'])
def transactions():
    cur = mysql.connection.cursor()  
    cur.execute("SELECT * FROM transactions")
    transaction_list=cur.fetchall()
    return render_template('transactions.html',place="transaction",transactions=transaction_list)
       
if __name__ == '__main__': 
    app.run(debug = True)  
