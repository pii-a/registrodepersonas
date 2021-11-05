from typing import Text
from flask import Flask, render_template , request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import Form, TextField ,validators, PasswordField, BooleanField
from flask_mysqldb import MySQL 
from flask import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='gpco'
mysql = MySQL(app)
flag=False

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['username'].upper()
        password = request.form['password']
    
        curs = mysql.connection.cursor()
        curs.execute("SELECT * FROM usuarios_login")
        for fila in curs:
            if fila [1] ==nombre and fila [2] ==password:
                global flag
                flag=True
                if flag ==True:
                    return redirect((url_for('registro')))
                else:
                    return redirect((url_for('login')))
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])   
def logout():
    print("volcado")
    global flag 
    flag = False
    return redirect((url_for('login')))


@app.route('/registro')
def registro():
    global flag 
    if flag ==True:
     return render_template('registro.html')
    else:
        return redirect((url_for('login')))


class ppm(Form):
    nombre = TextField('nombre', [validators.Length(min=2, max=25)])
    codigo = PasswordField('codigo', [validators.Length(min=2, max=25)])
    

@app.route('/añadir', methods=['POST'])
def añadir():
    form= ppm(request.form)
    if request.method =='POST' and form.validate():
        nombre = request.form['nombre'].upper()
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ppm (NAME , CODE) VALUES(%s, %s)',
        (nombre , codigo))
        mysql.connection.commit()
        return redirect(url_for('registro'))
    else: 
       flash('Registre un usuario o tarjeta')
       return redirect(url_for('registro')) 
    

        

@app.route('/extraer', methods=['GET'])
def extraer():
    if request.method =='GET':
        curs = mysql.connection.cursor()
        curs.execute("SELECT * FROM ppm")
        for x in curs:
            print(x)
    return redirect(url_for('registro')) 



if __name__ == '__main__':
    app.run(port = 3000, debug= True)

