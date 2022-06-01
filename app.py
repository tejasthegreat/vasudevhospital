from re import T
from flask import Flask,render_template,request,session,redirect
from datetime import datetime

import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY']='1234'


@app.route('/')
def index ():
    return render_template('home.html')


@app.route('/patient_register', methods=['GET', 'POST'])
def patient_register():
    if request.method=='GET':
        return render_template('patient_form.html')
    elif request.method=='POST':
        '''
        STEPS TO REGISTER
        1)GET ALL DATA FROM HTML
        2)CHECK WHEATHER THE USERNAME/EMAIL PRESENT IN THE DATABASE
        3)IF PRESENT- SEND 1 ERROR MESSAGE
        4)ELSE CHECK WHEATHER PASSWORD AND CONFIRM PASSWORD IS THE SAME
        5)IF NOT SEND ANOTHER ERROR MESSAGE
        6)INSERT ALL THE DATA IN THE DATABASE
        '''
        fname=request.form.get('firstname')
        lname=request.form.get('lastname')
        phonenumber=request.form.get('phonenumber')
        email=request.form.get('email')
        age=request.form.get('age')   
        password=request.form.get('password')
        confirmpassword=request.form.get('confirmpassword')
        gender=request.form.get('gender')
        city=request.form.get('city')
        conn=sqlite3.connect('database/vasudev_hospital.db')
        cur=conn.cursor()
        cur.execute('select email from userdata where email=?;',[email])
        email_db=cur.fetchone()
        if email_db!=None:
            error='email is alredy taken'
            return render_template('login.html',error=error)
        elif password==confirmpassword:
            error='registration successful'
            #insert query
            cur.execute('INSERT INTO userdata\
                (fname,lname,email,age,phonenumber,password,city,gender)\
                VALUES(?,?,?,?,?,?,?,?); ',\
                [fname,lname,email,age,phonenumber,password,city,gender])
            conn.commit()
            conn.close()
            return render_template('login.html',error=error)
        else:
            error='password mismatch'
            return render_template('patient_form.html',error=error)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method =='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        conn=sqlite3.connect('database/vasudev_hospital.db')
        cur=conn.cursor()
        password_db=cur.execute('select password from userdata where email=?;',[email]).fetchone()
        if password_db==None:
            error='invalied credinitials'
            return render_template('login.html')
        else:
            error='login successful , please select your date and time for your appointment'
            session['email']=email
            session ['login']=True

            return render_template('appointment.html',error=error)
    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html',message= 'you have successfully logged out')



@app.route('/patient_form', methods=['GET', 'POST'])
def patient_form():
    conn=sqlite3.connect('vasudev_hospital.db')
    cur=conn.cursor()
    if request.method=='GET':
        return render_template('patient_form.html')
    elif request.method=='POST':
        fname=request.form.get('firstname')
        lname=request.form.get('lastname')
        phonenumber=request.form.get('phonenumber')
        email=request.form.get('email')
        age=request.form.get('age')
        password=request.form.get('password')
        confirmpassword=request.form.get('confirmpassword')
        gender=request.form.get('gender')
        city=request.form.get('city')
        if password==confirmpassword:
            cur.execute('insert into userdata(fname,lname,email,age,city,gender,password,phonenumber)\
            values(?,?,?,?,?,?,?,?);\
               ',[fname,lname,email,age,city,gender,password,phonenumber])
        else:
            print('error')
            return render_template('patient_form.html',error='passord mismatch')
    conn.commit()
    conn.close()
    return 'sucsess'



@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if session.get('login')==None:
        return redirect('login')
    if request.method == 'GET':
        return render_template ('appointment.html')
    date=request.form.get('date')
    print(date)
    date_object=datetime.strptime(date,'%Y-%m-%d')
    print(date_object)
    date_format=datetime.strftime(date_object,'%d-%m-%Y')
    print(date_format)
    time=request.form.get('time')

    print(time)
    conn=sqlite3.connect('database/vasudev_hospital.db')
    cur=conn.cursor()
    userid=cur.execute('select userid from userdata where email = ?;', [session.get('email')]).fetchone()
    cur.execute('insert into appointment(userid,date,time) values(?,?,?);',[userid[0],date_format,time])
    conn.commit()
    conn.close()
    message='your appontment has been confirmed on '+date+'at '+time+'please be on schedule appointment time'
    return render_template('appointment.html',message=message)



@app.route('/allappointments', methods=['GET', 'POST'])
def allapoinments():
    if session.get('doctor_login')!=True:
        message='please authenticate yourself to view your appointments' 
        return render_template('doctor_login.html', message=message)
    conn=sqlite3.connect('database/vasudev_hospital.db')
    cur=conn.cursor()
    d=datetime.today()
    s=datetime.strftime(d,'%d-%m-%Y')
    print(s)
    records=cur.execute('select * from userdata inner join appointment on userdata.userid = appointment.userid order by date desc;').fetchall()
    conn.close()
    print (records)
    return render_template('allappointments.html',records=records)


@app.route('/myappointment')
def myappointment():
    conn=sqlite3.connect('database/vasudev_hospital.db')
    cur=conn.cursor()
    currentuser=session.get('email')
    records=cur.execute('select * from userdata inner join appointment on userdata.userid = appointment.userid where email = ? order by date desc;',[currentuser]).fetchall()
    conn.close()
    return render_template('myappointment.html',records=records)


@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method=='GET':
        return render_template('doctor_login.html')
    if request.method=='POST':
        admin_username='doctor@vasudev_hospital'
        admin_password='1234567'
        email=request.form.get('email')
        password=request.form.get('password')
        if email==admin_username and password==admin_password:
           message=' you have successfully logned in as a doctor'
           session['doctor_login']=True
        else:
            message='invalient credentials'
    return render_template('doctor_login.html',message=message)


@app.route('/to_do_list', methods=['GET', 'POST'])
def to_do_list():
    if request.method=='GET':

        return render_template('to_do_list.html')
    else:
        task=request.form.get('taskname')
        date=request.form.get('end_date')
        time=request.form.get('end_time')
        conn=sqlite3.connect('database/vasudev_hospital.db')
        cur=conn.cursor()
        cur.execute ('insert into to_do_list(taskname,end_date,end_time) values(?,?,?);',[task,date,time] )
        conn.commit()
        conn.close()
        message='task created successfully'
        return render_template('to_do_list.html',message=message)


@app.route('/view_to_do')
def view_to_do():
    conn=sqlite3.connect('database/vasudev_hospital.db')
    cur=conn.cursor()
    cur.execute('select * from to_do_list;')
    records=cur.fetchall()
    print (records)
    return render_template('view_to_do.html',x=records)





        

friends = ['ajay','vinay','sujay','suresh']

@app.route('/viewfriends')
def viewfriends():
    return render_template('home.html',friends=friends)



if __name__=='__main__':
    app.run(debug=True)