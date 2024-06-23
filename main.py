from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key="india"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='hr_erp_db'
mysql= MySQL(app)
 
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def aboutus():
    return render_template('aboutus.html')
@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')
@app.route('/contact')
def contactus():
    return render_template('contactus.html')
@app.route('/header')
def header():
    return render_template('header.html')
@app.route('/admindashboard',methods=['post'])
def admindashboard():
    U = request.form['txtUsername']
    P = request.form['txtPassword']
    if (U=="admin" and P=="super"):
        session["name"] = "Ram"
        session["login"] = U
        return render_template('admin_dashboard.html')
    else:
     msg = "Invaild Username and Password."
    return render_template("adminlogin.html",massage=msg)
@app.route('/addemp')
def addemp():
    return render_template('admin_Addemp.html')
@app.route('/searchemp')
def searchemp():
    return render_template('admin_Searchemp.html')
@app.route('/showemp')
def showemp():
    #Data connection open
    cur = mysql.connection.cursor()
    #Query Specification
    cur.execute('select empid,empname,designation from registration')
    emplist = cur.fetchall()
    return render_template('admin_Showemp.html',recordlist=emplist)

@app.route('/save',methods=['post'])
def save():
    i = request.form['txtEmpID']
    n = request.form['txtName']
    e = request.form['txtEmailID']
    m = request.form['txtMobileNO']
    d = request.form['txtDesignation']
    s = request.form['txtSalary']

    cur = mysql.connection.cursor()
    cur.execute('insert into registration(empid,empname,email,mobile,designation,salary ) values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))
    mysql.connection.commit()
    cur.close()
    return render_template('admin_reg_success.html')

@app.route('/admin_profile')
def admin_profile():
    id = request.args.get('eid')
    cur = mysql.connection.cursor()
    cur.execute('select empid,empname,email,mobile,designation,salary from registration where empid='+id)
    emplist = cur.fetchall()
    return render_template('admin_profile.html',recordlist=emplist)

@app.route('/admin_emp_update',methods=['post'])
def admin_update_success():
    i = request.form['txtEmpID']
    n = request.form['txtName']
    e = request.form['txtEmailID']
    m = request.form['txtMobileNO']
    d = request.form['txtDesignation']
    s = request.form['txtSalary']

    cur = mysql.connection.cursor()
    cur.execute('update registration set designation=%s,salary=%s,empname=%s,email=%s,mobile=%s where empid=%s',(d,s,n,e,m,i,))
    mysql.connection.commit()
    cur.close()
    return render_template('admin_emp_update_success.html')

@app.route('/admin_emp_delete')
def admin_emp_delete():
    i = request.args.get('id')
    cur = mysql.connection.cursor()
    cur.execute('delete from registration where empid= %s',(i,))
    mysql.connection.commit()
    cur.close()
    return render_template('/admin_emp_delete_success.html')

@app.route('/admin_emp_searchprocess',methods=['post'])
def admin_emp_searchprocess():
    n = request.form['txtName']
    print(n)
    cur = mysql.connection.cursor()
    q = "select * from registration where empname like'" +n+" %'"
    print(q)
    cur.execute(q)
    emplist = cur.fetchall()
    cur.close()
    return render_template('admin_emp_searchresult.html',recordlist=emplist)
@app.route('/logout')
def logout():
    session["name"]=None
    return render_template('adminlogin.html')
app.run(debug=True)