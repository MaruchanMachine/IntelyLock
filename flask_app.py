from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from models.ModelUser import ModelUser
from models.ModelAula1 import ModelAula1
from models.ModelAula2 import ModelAula2
from models.ModelAula3 import ModelAula3
from models.entities.User import User
from models.entities.Aula1 import Aula1
from datetime import datetime

import mysql.connector

app = Flask(__name__, static_url_path='/IntellyLock/IntellyLock - Equipo 7/IntelliLock/static')

current_datetime = datetime.now()
current_time = current_datetime.strftime('%H:%M:%S')

app.config['SECRET_KEY'] = 'mysecretkey'

app.config['MYSQL_HOST'] = 'BurritoLoco2000.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'BurritoLoco2000'
app.config['MYSQL_PASSWORD'] = '1234root'
app.config['MYSQL_mysql'] = 'BurritoLoco2000$flask_ingresos'

# mysql = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    database="BurritoLoco2000$flask_ingresos"
# )

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_mysql'] = 'BurritoLoco2000$flask_ingresos'

mysql = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(0, username, password)
        logged_user = ModelUser.login(mysql, user)

        if logged_user != None:
            if logged_user.password:
                cursor = mysql.connection.cursor()
                sql2 = """use BurritoLoco2000$flask_ingresos"""
                cursor.execute(sql2)
                cursor.execute('INSERT INTO user_accesoss(username, fecha, hora) VALUES (%s, %s, %s)',
                               [request.form['username'], current_datetime, current_time])
                mysql.connection.commit()

                session['user_details'] = {'username': logged_user.username}
                session['logged_in'] = True

                return redirect(url_for('accesar'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/cerrarPuerta', methods=['POST'])
def cerrarPuerta():
    cursor = mysql.connection.cursor()
    sql2 = """use BurritoLoco2000$flask_ingresos"""
    cursor.execute(sql2)
    cursor.execute("""UPDATE aula1 SET password = %s WHERE id= %s""", ('no', 2))
    mysql.connection.commit()
    puerta_estado = False
    session['puerta_estado'] = puerta_estado
    puerta_estado = session.get('puerta_estado', False)
    return render_template('accesar.html', puerta_estado=puerta_estado)


@app.route('/accesar', methods=['GET', 'POST'])
def accesar():
    if request.method == 'POST':
        aula1 = Aula1(0, 'aula1', request.form['password'])
        aula1_selected = ModelAula1.login(mysql, aula1)

        aula2 = Aula1(0, 'aula2', request.form['password'])
        aula2_selected = ModelAula2.login(mysql, aula2)

        aula3 = Aula1(0, 'aula3', request.form['password'])
        aula3_selected = ModelAula3.login(mysql, aula3)

        aula = request.form.get("aulas")
        cursor = mysql.connection.cursor()
        sql2 = """use BurritoLoco2000$flask_ingresos"""
        cursor.execute(sql2)
        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('no', 2))
        mysql.connection.commit()

        if 'logged_in' in session and session['logged_in']:
            if aula1_selected != None:
                if aula == "aula1":
                    if aula1_selected.password:
                        flash("The door is unlocked...")
                        puerta_estado = True
                        session['puerta_estado'] = puerta_estado
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('si', 2))
                        mysql.connection.commit()

                        user_details = session.get('user_details', None)
                        if user_details:
                            username = user_details['username']

                            cursor.execute(
                                'INSERT INTO aula_accesos(aula, username, fecha, hora) VALUES (%s, %s, %s, %s)',
                                ['aula1', username, current_datetime, current_time])
                            mysql.connection.commit()

                        return redirect(url_for('accesar'))
                    else:
                        flash("Invalid password...")
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('no', 2))
                        mysql.connection.commit()
                        return render_template('accesar.html')
            else:
                flash("Aula not found...")
                return render_template('accesar.html')
            if aula2_selected != None:
                if aula == "aula2":
                    if aula2_selected.password:
                        flash("The door is unlocked...")
                        # return jsonify(request.form['password'])
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('si', 2))
                        mysql.connection.commit()

                        user_details = session.get('user_details', None)
                        if user_details:
                            username = user_details['username']

                            cursor.execute(
                                'INSERT INTO aula_accesos(aula, username, fecha, hora) VALUES (%s, %s, %s, %s)',
                                ['aula2', username, current_datetime, current_time])
                            mysql.connection.commit()

                        return redirect(url_for('accesar'))

                    else:
                        flash("Invalid password...")
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('no', 2))
                        mysql.connection.commit()
                        return render_template('accesar.html')
            else:
                flash("Aula not found...")
                return render_template('accesar.html')

            if aula3_selected != None:
                if aula == "aula3":
                    if aula3_selected.password:
                        flash("The door is unlocked...")
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('si', 2))
                        mysql.connection.commit()

                        user_details = session.get('user_details', None)
                        if user_details:
                            username = user_details['username']

                            cursor.execute(
                                'INSERT INTO aula_accesos(aula, username, fecha, hora) VALUES (%s, %s, %s, %s)',
                                ['aula3', username, current_datetime, current_time])
                            mysql.connection.commit()

                        return redirect(url_for('accesar'))
                    else:
                        flash("Invalid password...")
                        cursor = mysql.connection.cursor()
                        sql2 = """use BurritoLoco2000$flask_ingresos"""
                        cursor.execute(sql2)
                        cursor.execute("""UPDATE aula2 SET password = %s WHERE id= %s""", ('no', 2))
                        mysql.connection.commit()
                        return render_template('accesar.html')
            else:
                flash("Aula not found...")
                return render_template('accesar.html')
    else:
        puerta_estado = session.get('puerta_estado', False)
        return render_template('accesar.html', puerta_estado=puerta_estado)


@app.route('/verAccesosSistema', methods=['GET'])
def verAccesosSistema():
    cursor = mysql.connection.cursor()
    cursor.execute("USE BurritoLoco2000$flask_ingresos")
    cursor.execute("SELECT username, fecha, hora FROM user_accesoss")
    data = cursor.fetchall()
    cursor.close()
    return render_template('verAccesosSistema.html', data=data)


@app.route('/verAccesosAulas', methods=['GET'])
def verAccesosAulas():
    cursor = mysql.connection.cursor()
    cursor.execute("USE BurritoLoco2000$flask_ingresos")
    cursor.execute("SELECT aula, username, fecha, hora FROM aula_accesos")
    data = cursor.fetchall()
    cursor.close()
    return render_template('verAccesosAulas.html', data=data)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
