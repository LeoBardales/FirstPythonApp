import string
import random
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import smtplib
import email.message
server = smtplib.SMTP('smtp.gmail.com:587')

from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)
csrf = CSRFProtect()
# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asebep'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
login_manager_app = LoginManager(app)




# settings
app.secret_key = "mysecretkey"
app.secret_key = "caircocoders-ednalan"
app.secret_key = "B!1w8NAt1T^%kvhUI*S^"

#============================================================Elementos Login============================================================#
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Routes to Render Something
@app.route('/')
def login():
    return render_template("auth/index.html")



@app.route('/acces',methods=["POST","GET"])
def acces():
    correo = request.form['email']
    cont = request.form['password']
    user = User(0,correo,cont,'',0,0)
    logged_user = ModelUser.login(mysql, user)

    if logged_user != None:
        if logged_user.password:
            login_user(logged_user)
            if logged_user.activo == 'SI':
                if int(logged_user.usertype) == 1:
                    return redirect(url_for('home'))

                else :
                    if int(logged_user.usertype) == 2:
                        return redirect(url_for('homeEstudiante'))
                    else:
                        if int(logged_user.usertype) == 3:
                            return redirect(url_for('homeRoot'))
                        else:
                             return logout()
            else:
                flash("Este usuario esta inactivo...")
                return logout()
        else:
            flash("Contraseña incorrecta..")
            return redirect(url_for('login'))
    else:
        flash("Usuario incorrecto...")
        return redirect(url_for('login'))


#Registrar Usuario-----------------------------------------------------------------------------
@app.route("/Recuperar_Contra",methods=["POST","GET"])
def Recuperar_Contra():
    if request.method == 'POST':
        Correo = request.form['email']
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE Email = '{}' ".format(Correo)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row != None:
            id=row['UserId']
            characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
            random.shuffle(characters)
            password = []
            for i in range(8):
                password.append(random.choice(characters))
            random.shuffle(password)
            contra="".join(password)
            Contra=generate_password_hash(contra)
            print('La nueva contrasena es: ',contra)
            cur = mysql.connection.cursor()
            cur.execute("update users set Password=%s where UserId=%s", (Contra,id))
            mysql.connection.commit()
            flash('Se envio su nueva contraseña a su correo electronico')
            email_content = """<html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

            <title>ASEBEP</title>
            
        </head>

        <body>


            <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4">
                <tr>
                    <td>
                        
                        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
                            <tr>
                                <td>
                                    <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                                        <tr>
                                            <td width="570" align="center" bgcolor="#cda434">
                                                <h1 color="ffffff">Nueva contraseña en la Plataforma ASEBEP UNAH-VS</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="570" align="left" bgcolor="#cda434">
                                                <p>Usted solicitud que se le diera una nueva contraseña para recuperar su cuenta</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="150" valign="top" bgcolor="d0d0d0" >
                                                <img src="https://asebepunahcu.files.wordpress.com/2017/09/logo-asebep.png?w=294" width="150"height="150" />
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="200" valign="top">
                                                <h3 align="center"><b>ASEBEP UNAH-VS</b></h3>
                                                <br>Su nueva contraseña es:</br> 
                                                <br><b>{}</b> </br>
                                                <br> Recuerde que usted puede cambiar la contraseña dentro de la plataforma ingresando a la pestaña mis datos ahi podra ver y cambiar su información</br>
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>


                        </table>
                        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
                            <tr>
                                <td bgcolor="#40CFFF" align="center">
                                    <p id="bajo">Diseñado para una mejor experiencia de nuestros Usuarios</p>
                                    <p ><a href="https://www.facebook.com/Asebep-Unah-Vs-101545674954541">Facebook ASEBEP</a> | <a href="https://www.instagram.com/asebepvs/">Instagram ASEBEP</a> </p>
                                </td>
                            </tr>
                        </table><!-- top message -->
                    </td>
                </tr>
            </table><!-- wrapper -->

        </body>

        </html>""".format(contra)
            msg = email.message.Message()
            msg['Subject'] = 'Recuperacion de su contraseña'
            msg['From'] = 'asabepunahvs@gmail.com'
            msg['To'] = Correo
            password = "Ae$Tb5Waf3EEq"
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8').strip())
            
            return redirect(url_for('login'))
        else:
            flash('El usuario no existe')
    return redirect(url_for('login'))


#Registrar Usuario-----------------------------------------------------------------------------
@app.route("/Registro_Usuario",methods=["POST","GET"])
def Registro_Usuario():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Cuenta = request.form['Cuenta']
        Telefono = request.form['Telefono']
        Correo = request.form['Correo']
        BecaId = request.form['Beca']
        CarreraId = request.form['Carrera']
        ano = request.form['ano']
        periodo = request.form['Periodo']
        obs="Inicio el beneficio el "+periodo+" del año "+ano
        #Contra = request.form['password2']
        Contra=""

        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT count(NCuenta) as Max FROM estudiantes WHERE NCuenta = %s and Registrado='NO'",(Cuenta,))
        data = cur1.fetchall()
        cur1.close()
        for p in data :
            exis=p['Max']
        
        if(int(exis)>0):
            cur1 = mysql.connection.cursor()
            cur1.execute('SELECT count(UserId) as Max FROM users WHERE Email = %s',(Correo,))
            data = cur1.fetchall()
            cur1.close()
            for p in data :
                exis=p['Max']

            
            if(exis==0):
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
                random.shuffle(characters)
                password = []
                for i in range(8):
                    password.append(random.choice(characters))
                random.shuffle(password)
                contra="".join(password)
                Contra=generate_password_hash(contra)
	                     
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(Nombre, Email, Password, IdUserType, Activo) VALUES (%s,%s,%s,2,'SI')", (Nombre,Correo,Contra))
                mysql.connection.commit()
                cur1 = mysql.connection.cursor()
                cur1.execute('SELECT UserId as Max FROM users WHERE Email = %s',(Correo,))
                data = cur1.fetchall()
                cur1.close()
                for p in data :
                    UserId=p['Max']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE estudiantes SET BecaId=%s,CarreraId=%s,UserId=%s,Telefono=%s, Registrado='SI', Observaciones=%s WHERE NCuenta = %s",(BecaId,CarreraId,UserId,Telefono,obs,Cuenta))
                mysql.connection.commit()
                success_message = 'Usuario creado con exito'

                email_content = """<html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

            <title>ASEBEP</title>
            
        </head>

        <body>


            <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4">
                <tr>
                    <td>
                        
                        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
                            <tr>
                                <td>
                                    <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                                        <tr>
                                            <td width="570" align="center" bgcolor="#cda434">
                                                <h1 color="ffffff">Bienvenidos a la plataforma ASEBEP UNAH-VS</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="570" align="left" bgcolor="#cda434">
                                                <p>Usted se registro es nuestra plataforma</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="150" valign="top" bgcolor="d0d0d0" >
                                                <img src="https://asebepunahcu.files.wordpress.com/2017/09/logo-asebep.png?w=294" width="150"height="150" />
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="200" valign="top">
                                                <h3 align="center"><b>ASEBEP UNAH-VS</b></h3>
                                                <br><b>{}</b> ustes se registro en la plataforma para estudiantes ASEBEP, su contraseña es:</br>
                                                <br> <b>{}</b> </br>
                                                <br> Recuerde que usted puede cambiar la contraseña dentro de la plataforma ingresando a la pestaña mis datos ahi podra ver y cambiar su información</br>
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>


                        </table>
                        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
                            <tr>
                                <td bgcolor="#40CFFF" align="center">
                                    <p id="bajo">Diseñado para una mejor experiencia de nuestros Usuarios</p>
                                    <p ><a href="https://www.facebook.com/Asebep-Unah-Vs-101545674954541">Facebook ASEBEP</a> | <a href="https://www.instagram.com/asebepvs/">Instagram ASEBEP</a> </p>
                                </td>
                            </tr>
                        </table><!-- top message -->
                    </td>
                </tr>
            </table><!-- wrapper -->

        </body>

        </html>""".format(Nombre,contra)
                msg = email.message.Message()
                msg['Subject'] = 'Confirmacion de Registro en Plataforma ASEBEP UNAH-VS'
                msg['From'] = 'asabepunahvs@gmail.com'
                msg['To'] = Correo
                password = "Ae$Tb5Waf3EEq"
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()
                # Login Credentials for sending the mail
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8').strip())
                
            else:
                success_message = 'Error: El Correo ya existe'
            
            flash(success_message)
            return redirect(url_for('login'))
        else:
            flash("Error: Esta Cuenta no tiene acceso al Registro en nuestra plataforma")
            return redirect(url_for('login'))
#generar contrasena
	#Npassword=generate_password_hash(contra)

#=====================================================================Elementos Root=========================================================================#
@app.route('/Index')
@login_required
def homeRoot():
    if current_user.usertype == 3:
        user = current_user.id
        if user == None:
            return login()   
        else:
            return render_template("root/index.html")
    else:
        return logout()	

#Llenar tabla de usuarios---------------------------------------------------------------------------------------
@app.route("/TablaUsuarios",methods=["POST","GET"])
@login_required
def TablaUsuarios():
    if current_user.usertype == 3:
        if request.method == 'POST':   
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM users where IdUserType=1 ORDER by Nombre ASC"
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('root/TablaUsuarios.html', listas=programming)})
    else:
        return logout()

#ver Administrador------------------------------------------------------------------------------------
@app.route('/admin_edit/<id>')
@login_required
def admin_edit(id):
    if current_user.usertype == 3:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users where UserId={}".format(id)
        cur.execute(query)
        programming = cur.fetchall()
            
        return render_template("root/Datos_Admin.html",listas=programming)
    else:
        return logout
#Registrar nuevo administrador---------------------------------------------------------------------------------------------------------
@app.route("/RegistroAdmin",methods=["POST","GET"])
@login_required
def RegistroAdmin():
    if current_user.usertype == 3:
        if request.method == 'POST': 
            Nombre = request.form['Nombre']
            Correo = request.form['Correo']
            cursor = mysql.connection.cursor()
            sql = "SELECT *FROM users where Email = '{}'".format(Correo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                flash('Error: El correo ya existe')
                return redirect(url_for('homeRoot'))
            else:
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
                random.shuffle(characters)
                password = []
                for i in range(8):
                    password.append(random.choice(characters))
                random.shuffle(password)
                contra="".join(password)
                Contra=generate_password_hash(contra)
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(Nombre, Email, Password, IdUserType, Activo) VALUES (%s,%s,%s,1,'SI')", (Nombre,Correo,Contra))
                mysql.connection.commit()
                flash('Usuario creado con exito')
                email_content = """<html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

            <title>ASEBEP</title>
            
        </head>

        <body>


            <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4">
                <tr>
                    <td>
                        
                        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
                            <tr>
                                <td>
                                    <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                                        <tr>
                                            <td width="570" align="center" bgcolor="#cda434">
                                                <h1 color="ffffff">Bienvenidos a la plataforma ASEBEP UNAH-VS</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="570" align="left" bgcolor="#cda434">
                                                <p>Usted ha sido registrado es nuestra plataforma como administrador</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="150" valign="top" bgcolor="d0d0d0" >
                                                <img src="https://asebepunahcu.files.wordpress.com/2017/09/logo-asebep.png?w=294" width="150"height="150" />
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="200" valign="top">
                                                <h3 align="center"><b>ASEBEP UNAH-VS</b></h3>
                                                <br><b>{}</b> ustes ha sido registrado en la plataforma como Administrador ASEBEP, su contraseña es:</br>
                                                <br> <b>{}</b> </br>
                                                <br> Recuerde que usted puede cambiar la contraseña dentro de la plataforma ingresando a la pestaña mis datos ahi podra ver y cambiar su información</br>
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>


                        </table>
                        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
                            <tr>
                                <td bgcolor="#40CFFF" align="center">
                                    <p id="bajo">Diseñado para una mejor experiencia de nuestros Usuarios</p>
                                    <p ><a href="https://www.facebook.com/Asebep-Unah-Vs-101545674954541">Facebook ASEBEP</a> | <a href="https://www.instagram.com/asebepvs/">Instagram ASEBEP</a> </p>
                                </td>
                            </tr>
                        </table><!-- top message -->
                    </td>
                </tr>
            </table><!-- wrapper -->

        </body>

        </html>""".format(Nombre,contra)
                msg = email.message.Message()
                msg['Subject'] = 'Confirmacion Registro de Administrador en Plataforma ASEBEP UNAH-VS'
                msg['From'] = 'asabepunahvs@gmail.com'
                msg['To'] = Correo
                password = "Ae$Tb5Waf3EEq"
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()
                # Login Credentials for sending the mail
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8').strip())
                return redirect(url_for('homeRoot'))

#=====================================================================Elementos Administrador=====================================================================#
#--------------------------------------------------Pagina de Inicio -------------------------------------#
#ruta inicio Admin--------------------------------------------------------
@app.route('/Inicio')
@login_required
def home():
    if current_user.usertype == 1:
        user = current_user.id
        if user == None:
            return login()   
        else:
            return render_template("admin/index.html")
    else:
        return logout()


@app.errorhandler(401)
def NoAutorizado(error):
    return logout(),401

#filtrar tabla actividades por mes y año-------------------------------------
@app.route("/FiltroActividades",methods=["POST","GET"])
def FiltrarActividades():
        if request.method == 'POST':  
            mes=request.form['mes']  
            ano=request.form['ano']
            if(mes=='0' and ano=='0'):
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT * FROM actividades WHERE YEAR(Fecha)= YEAR(curdate()) and MONTH(Fecha)=MONTH(curdate()) and day(Fecha)>= Day(curdate()) ORDER by Fecha,Hora_I ASC"
                cur.execute(query)
                programming = cur.fetchall()

            else:  
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT * FROM actividades WHERE YEAR(Fecha)='{}' and MONTH(Fecha)='{}' ORDER by Fecha,Hora_I ASC".format(ano,mes)
                cur.execute(query)
                programming = cur.fetchall()
    
            return jsonify({'data': render_template('complementos/Actividades.html', listas=programming)})
    
#filtrar tabla actividades por Dia---------------------------------------------
@app.route("/FiltroActividadesDia",methods=["POST","GET"])
def FiltroActividadesDia():
        if request.method == 'POST':  
            Fecha=request.form['Fecha']  

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM actividades WHERE Fecha='{}' ORDER by Fecha,Hora_I ASC".format(Fecha)
            cur.execute(query)
            programming = cur.fetchall()
    
            return jsonify({'data': render_template('complementos/Actividades.html', listas=programming)})
    

#Eliminar actividades desde Inicio---------------------------------------------
@app.route("/Eliminar_Registro/<id>",methods=["POST","GET"])
def Eliminar_Reg(id):
        cur = mysql.connection.cursor()
        cur.execute("delete from actividades WHERE idActividades=%s",(id,))
        mysql.connection.commit()

        cur1 = mysql.connection.cursor()
        cur1.execute("delete from registro WHERE idActividades=%s",(id,))
        mysql.connection.commit()
        success_message="Actividad Eliminada con Exito"
        flash(success_message)

        return redirect(url_for('home'))
    


#Llenar bandeja de reclamos-------------------------------------------------------------------------------
@app.route("/bandeja_reclamos",methods=["POST","GET"])
def bandeja_reclamos():
        if request.method == 'POST':  

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_reclamos ORDER by Fecha ASC"
            cur.execute(query)
            programming = cur.fetchall()
    
            return jsonify({'data': render_template('complementos/bandeja_reclamos.html', listas=programming)})
   

#Llenar bandeja de reclamos-------------------------------------------------------------------------------
@app.route("/numero_reclamos",methods=["POST","GET"])
def numero_reclamos():
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(idreclamos) as Cant FROM reclamos WHERE Visto='NO'"
        cur.execute(query)
        programming = cur.fetchall()
            
        return jsonify({'data': render_template('complementos/reclamos.html', listas=programming)})
   

#Marca como visto---------------------------------------------------------------------------------------
@app.route('/marcar_visto/<id>')
def marcar_visto(id):
    if current_user.usertype == 1:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE reclamos SET Visto='SI' WHERE idreclamos=%s", (id,))
        mysql.connection.commit()
    
        return redirect(url_for('home'))
    else:
        return logout()


#----------------------------------------------------------------------------Registrar Actividad----------------------------------------------------------------------#
#Agregar Actividad----------------------------------------------------------------------------------------------------
@app.route('/Nueva_Actividad')
@login_required
def create():
    if current_user.usertype == 1:
        return render_template("admin/create.html")
    return logout()

#evento crear--------------------------------------------------------------------------------------------------------
@app.route('/Registro', methods=['POST','GET'])
@login_required
def registro():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Actividad1 = request.form['Actividad']
            Encargado = request.form['Encargado']
            HoraI = request.form['HoraI']
            HoraF = request.form['HoraF']
            Fecha = request.form['Fecha']
            Horas = request.form['Horas']
            Acceso = request.form['Acceso']
            Cupos = request.form['Cupos']
            Descripcion = request.form['Descripcion']


            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO actividades (Actividad, Encargado, Hora_I, Hora_F,Fecha, Horas,Acceso,Cupos,Descripcion,Inscritos) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,0)", (Actividad1, Encargado, HoraI,HoraF,Fecha,Horas,Acceso,Cupos,Descripcion))
            mysql.connection.commit()
            cur1 = mysql.connection.cursor()
            cur1.execute('SELECT max(idActividades) as Max FROM actividades')
            data = cur1.fetchall()
            cur1.close()

            for p in data :
                codigo=p['Max']

            success_message="Actividad Creada"
            flash(success_message)
    
            return redirect(url_for("get_actividad",id=codigo))
    else:
        return logout()

#Editar Actividad----------------------------------------------------------------------------------------
@app.route('/actividad_edit/<id>', methods=['POST','GET'])
@login_required
def get_actividad(id):
    if current_user.usertype == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM actividades WHERE idActividades= %s ", (id,))
        mysql.connection.commit()
        Lista = cur.fetchall()
        cur.close()
        
        for lista in Lista:
            Horaf=lista['Hora_F']
            HoraI=lista['Hora_I']
        
        
        hora1 = datetime.strptime(str(HoraI), "%X").time()
        hora2 = datetime.strptime(str(Horaf), "%X").time()

        if(hora1 < datetime.strptime("10:00:00", "%X").time()):
            HoraI="0"+str(HoraI)

        if(hora2 < datetime.strptime("10:00:00", "%X").time()):
            Horaf="0"+str(Horaf)

        for lista in Lista:
            lista['Hora_F']=Horaf
            lista['Hora_I']=HoraI

        return render_template('admin/actividad_edit.html',Actividades=Lista)
    else:
        return logout()


#elimar actividad------------------------------------------------------------------------------------------
@app.route("/Eliminar_Registro",methods=["POST","GET"])
@login_required
def Eliminar_Registro():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Codigo = request.form['idActividad']
            print('Paso Esto se elimino toda la actividad')

            cur = mysql.connection.cursor()
            cur.execute("delete from actividades WHERE idActividades=%s",(Codigo,))
            mysql.connection.commit()

            cur1 = mysql.connection.cursor()
            cur1.execute("delete from registro WHERE idActividades=%s",(Codigo,))
            mysql.connection.commit()

            success_message="Actividad Eliminada con Exito"
            flash(success_message)

            return redirect(url_for('home'))
    else:
        return logout()

#Actualizar Registro-------------------------------------------------------------------------------------------------
@app.route("/Actualizar_Registro",methods=["POST","GET"])
@login_required
def actulizar_Registro():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Codigo = request.form['idActividad']
            Actividad1 = request.form['Actividad']
            Encargado = request.form['Encargado']
            HoraI = request.form['HoraI']
            HoraF = request.form['HoraF']
            Fecha = request.form['Fecha']
            Horas = request.form['Horas']
            Cupos = request.form['Cupos']
            Acceso = request.form['Acceso']
            Descripcion = request.form['Descripcion']
            comp=1

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT (cupos) as result,Inscritos  FROM actividades WHERE idActividades='{}'".format(Codigo)
            cur.execute(query)
            programming = cur.fetchall()

            for lista in programming:
                cup=lista['result']
                Ins=lista['Inscritos']

            if(int(Cupos)>=int(cup)):
                comp=1;    
            else:
                comp=int(Cupos)-int(Ins)  
            

            if(comp>=0):
                success_message="Actividad Actualizado con Exito"
            else:
                result=int(Ins)-int(Cupos)
                cur = mysql.connection.cursor()
                cur = mysql.connection.cursor()
                cur.execute("DELETE from registro WHERE idActividades=%s order by RegistroId DESC limit %s", (Codigo,result))
                mysql.connection.commit()
                cur1 = mysql.connection.cursor()
                cur1.execute("UPDATE actividades set Inscritos=%s WHERE idActividades=%s ", (Cupos,Codigo))
                mysql.connection.commit()
                success_message="Se eliminaron los ultimos estudiantes inscritos"



            cur = mysql.connection.cursor()
            cur.execute("UPDATE actividades SET Cupos=%s, Acceso=%s , Descripcion=%s,Actividad=%s,Encargado=%s,Fecha=%s,Hora_I=%s,Hora_F=%s,Horas=%s WHERE idActividades=%s", (Cupos,Acceso,Descripcion,Actividad1, Encargado,Fecha, HoraI,HoraF,Horas,Codigo))
            mysql.connection.commit()
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_registro WHERE idActividades='{}'".format(Codigo)
            cur.execute(query)
            programming = cur.fetchall()
            flash(success_message)
            return jsonify({'data': render_template('complementos/msg.html', programming=programming)})
    else:
        return logout()

#Eliminar Cuenta de Tabla de registro------------------------------------------------------------------------------------------------------------------------------
@app.route("/Eliminar_Cuenta/<id>/<idr>",methods=["POST","GET"])
def Eliminar_Cuenta(id,idr):
    
        cur = mysql.connection.cursor()
        cur.execute("delete from registro WHERE RegistroId=%s",(idr,))
        mysql.connection.commit()
        
        cur1 = mysql.connection.cursor()
        cur1.execute("UPDATE actividades SET Inscritos = Inscritos - 1  WHERE idActividades=%s", (id,))
        mysql.connection.commit()
        flash('La cuenta fue eliminada de los participantes')

        return redirect(url_for("get_actividad",id=id))



#actualizar tabla de participantes de la actividad---------------------------------------------------------------------------------
@app.route("/Tabla",methods=["POST","GET"])
def actulizar():
    if request.method == 'POST':
        Codigo = request.form['idActividad']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM view_registro WHERE idActividades='{}'".format(Codigo)
        cur.execute(query)
        programming = cur.fetchall()
        return jsonify({'data': render_template('complementos/add_cuenta.html', programming=programming)})

#registrar cuenta-------------------------------------------------------------------------------------------------------
@app.route("/add_cuenta",methods=["POST","GET"])
@login_required
def add_cuenta():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Codigo = request.form['idActividad']
            Cuenta = request.form['Cuenta']

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "select COUNT(EstudiantesId) as count from estudiantes WHERE NCuenta='{}'".format(Cuenta)
            cur.execute(query)
            programming = cur.fetchall()
            for p in programming:
                exis=p['count']

            if(exis==0):
                    success_message="Esta cuenta no esta registrada"
            
            else:
                cur1 = mysql.connection.cursor()
                cur1.execute('SELECT EstudiantesId FROM estudiantes WHERE NCuenta= %s',(Cuenta,))
                data = cur1.fetchall() 
                cur1.close()
                
                for p in data :
                    IdEstudiante=p['EstudiantesId']
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "select COUNT(EstudiantesId) as count from registro where idActividades='{}' and EstudiantesId='{}'".format(Codigo,IdEstudiante)
                cur.execute(query)
                programming = cur.fetchall()
                for p in programming:
                    exis=p['count']
                if exis==0 :
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    query = "SELECT (Cupos-Inscritos) as Cupos from actividades WHERE idActividades='{}'".format(Codigo)
                    cur.execute(query)
                    programming = cur.fetchall()
                    for p in programming:
                        cupos=p['Cupos']
                    if cupos>0:
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO registro (idActividades, EstudiantesId) VALUES (%s,%s)", (Codigo,IdEstudiante))
                        mysql.connection.commit()
                        cur1 = mysql.connection.cursor()
                        cur1.execute("UPDATE actividades SET Inscritos = Inscritos + 1  WHERE idActividades=%s", (Codigo,))
                        mysql.connection.commit()
                        success_message="Inscrito con exito"
                    else:
                        success_message="Ya no hay cupos en esta actividad"
                else:
                    success_message="Esta cuenta ya esta registrada"
    
                
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_registro WHERE idActividades='{}'".format(Codigo)
            cur.execute(query)
            programming = cur.fetchall()
            
            flash(success_message)
            return jsonify({'data': render_template('complementos/add_cuenta.html', programming=programming)})
    else:
        return logout()




#------------------------------------------------------Estudiantes--------------------------------------------------#
#ruta ver estudiantes--------------------------------------------------------------------------
@app.route('/Estudiantes')
@login_required
def ver_estudiantes():
    if current_user.usertype == 1:
        user = current_user.id
        cur1 = mysql.connection.cursor()
        cur1.execute('SELECT Nombre FROM users WHERE UserId= %s',(user,))
        data = cur1.fetchall()
        cur1.close()
        return render_template("admin/estudiantes.html",nombre=data)
    else:
        return logout()

#lista estudiantes---------------------------------------------------------------------------------
@app.route("/TablaEstudiantes",methods=["POST","GET"])
@login_required
def estudiantes():
    if current_user.usertype == 1:
        if request.method == 'POST':   
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_estudiantes ORDER by Nombre ASC"
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/Lista_Estudiantes.html', listas=programming)})
    else:
        return logout()

#Buscar en Lista de Estudiantes--------------------------------------------------------------------
@app.route("/Busqueda_Estudiante",methods=["POST","GET"])
@login_required
def Busqueda_Estudiante():
    if current_user.usertype == 1:
        if request.method == 'POST':  
            Busqueda=request.form['Busqueda']  
            
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_estudiantes as v WHERE v.NCuenta LIKE '%{}%' or v.Nombre LIKE '%{}%'".format(Busqueda,Busqueda)
            cur.execute(query)
            programming = cur.fetchall()
    
            return jsonify({'data': render_template('complementos/Lista_Estudiantes.html', listas=programming)})
    return logout()

#ver estudiantes------------------------------------------------------------------------------------
@app.route('/estudiantes_edit/<id>')
@login_required
def edit_estudiante(id):
    if current_user.usertype == 1:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM view_estudiantes where EstudiantesId={}".format(id)
        cur.execute(query)
        programming = cur.fetchall()
            
        return render_template("admin/estudiante_edit.html",listas=programming)
    else:
        return logout()

#llenar select de tipos de beca-----------------------------------------------------------------------
@app.route("/llenar_becas",methods=["POST","GET"])
def llenar_becas():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM beca order by Tipo ASC"
    cur.execute(query)
    programming = cur.fetchall()
    return jsonify({'data': render_template('complementos/llenar_becas.html', listas=programming)})

#llenar select de carreras ---------------------------------------------------------------------------
@app.route("/llenar_carreras",methods=["POST","GET"])
def llenar_carreras():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM carrera order by Carrera ASC"
    cur.execute(query)
    programming = cur.fetchall()
    return jsonify({'data': render_template('complementos/llenar_carreras.html', listas=programming)})

#llenar tabla de informes ---------------------------------------------------------------------------
@app.route("/tabla_informes",methods=["POST","GET"])
@login_required
def tabla_informes():
    if current_user.usertype == 1:
        ano=request.form['ano1']
        print(ano) 
        if(int(ano)==0):
            idestudiante=request.form['EstudiantesId']  
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM informes where EstudiantesId={} and ano= YEAR(curdate())".format(idestudiante)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/informes.html', listas=programming)})
        else:
            idestudiante=request.form['EstudiantesId']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM informes where EstudiantesId={} and ano= '{}'".format(idestudiante,ano)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/informes.html', listas=programming)})
    else:
        idestudiante=current_user.eid
        ano=request.form['ano'] 
        if int(ano)==0:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM informes where EstudiantesId={} and ano= YEAR(curdate())".format(idestudiante)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/informes.html', listas=programming)})
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM informes where EstudiantesId={} and ano= '{}'".format(idestudiante,ano)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/informes.html', listas=programming)})

#Actualizar Estudiante desde administrador----------------------------------------------------------------
@app.route("/Actualizar_Estudiante",methods=["POST","GET"])
@login_required
def Actualizar_Estudiante():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Nombre = request.form['Nombre']
            Cuenta = request.form['Cuenta']
            Telefono = request.form['Telefono']
            Correo = request.form['Correo']
            BecaId = request.form['Beca']
            CarreraId = request.form['Carrera']
            Activo = request.form['Activo']
            Seguimiento = request.form['Seguimiento']
            EstudiantesId = request.form['EstudiantesId']
            UserId = request.form['UserId']
            Observaciones = request.form['Observaciones']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET Nombre=%s,Email=%s,Activo=%s WHERE UserId=%s", (Nombre,Correo,Activo,UserId))
            mysql.connection.commit()
            
            cur1 = mysql.connection.cursor()
            cur1.execute("UPDATE estudiantes SET NCuenta=%s,BecaId=%s,CarreraId=%s,Seguimiento=%s,Telefono=%s,Observaciones=%s WHERE EstudiantesId=%s",(Cuenta,BecaId,CarreraId,Seguimiento,Telefono,Observaciones,EstudiantesId))
            mysql.connection.commit()
            flash('Datos Actualizados con exito')
            #return edit_estudiante(EstudiantesId)
            return redirect(url_for("edit_estudiante",id=EstudiantesId))
    else:
        return logout()

#llamar a registro Estudiantes desde Administrador-----------------------------------------------------------
@app.route('/Registro_Estudiantes/<id>',methods=["POST","GET"])
@login_required
def registro_estudiante(id):
    if current_user.usertype == 1:
        cur1 = mysql.connection.cursor()
        cur1.execute('SELECT Nombre,u.UserId,EstudiantesId FROM users as u INNER JOIN estudiantes as e on u.UserId=e.UserId  WHERE e.EstudiantesId= %s',(id,))
        data = cur1.fetchall()
        cur1.close()
        return render_template("admin/registro_estudiantes.html",nombre=data)
    else:
        return logout()

#llamar a tabla registro estudiante-------------------------------------------------------------------------
@app.route("/Tabla_Horas",methods=["POST","GET"])
def Tabla_Horas():
    if request.method == 'POST':
        Codigo = request.form['EstudiantesId']
        mes = request.form['mes']
        ano=request.form['ano']
        if(mes=='0' and ano=='0'):
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)=MONTH(CURRENT_DATE()) and Year(Fecha)=Year(CURRENT_DATE()) ORDER by Fecha,Hora_I ASC".format(Codigo)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/tablas_horas.html', programming=programming)})
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)='{}' and Year(Fecha)='{}'".format(Codigo,mes,ano)
            cur.execute(query)
            programming = cur.fetchall()
            return jsonify({'data': render_template('complementos/tablas_horas.html', programming=programming)})  




#----------------------------------------------Agregar Cuenta ,methods=["POST","GET"]-------------------------------------------------------------------
@app.route('/agregar_cuenta')
def agregar_cuenta():
    if current_user.usertype == 1:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT *FROM estudiantes WHERE Registrado = 'NO'"
        cur.execute(query)
        programming = cur.fetchall()
        return render_template("admin/Agregar_Cuenta.html", programming=programming)
    else:
        return logout()

#agregar cuenta para registro de usuarios-----------------------------------------------------------------------------------
@app.route('/agregar',methods=["POST","GET"])
def agregar():
    if current_user.usertype == 1:
        if request.method == 'POST':
            Cuenta = request.form['Cuenta']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT COUNT(EstudiantesId) as existe FROM estudiantes WHERE NCuenta =  '{}'".format(Cuenta)
            cur.execute(query)
            programming = cur.fetchall()
            for lista in programming:
                existe=lista['existe']

            if(existe>0):
                flash("Esta Cuenta ya esta Registrada")
                return agregar_cuenta()
            else:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO estudiantes(NCuenta,Registrado,BecaId,CarreraId,UserId,Seguimiento,Telefono,Observaciones) VALUES (%s,'NO',0,0,0,'','','')", (Cuenta,))
                mysql.connection.commit()
                flash("Registrada con exito")
                #return agregar_cuenta()
                return redirect(url_for("agregar_cuenta"))
    else:
        return logout()

#eliminar cuenta para registro------------------------------------------------------------------------------------------------------
@app.route('/eliminar/<id>',methods=["POST","GET"])
def eliminar(id):
    if current_user.usertype == 1:
        cur = mysql.connection.cursor()
        cur.execute( "DELETE from estudiantes WHERE EstudiantesId= %s", (id,))
        mysql.connection.commit()
        flash("Registro Eliminado con exito")
        return redirect(url_for("agregar_cuenta"))
    return logout()

#ver Datos Admin------------------------------------------------------------------------------------
@app.route('/datos_admin')
@login_required
def datos_admin():
    if current_user.usertype == 1:
        user=current_user.id
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users where UserId={}".format(user)
        cur.execute(query)
        programming = cur.fetchall()
            
        return render_template("admin/Mis_Datos.html",listas=programming)
    else:
        return logout()

#Actualizar Datos Admin------------------------------------------------------------------------------------
@app.route('/actualizar_admin',methods=["POST","GET"])
@login_required
def actualizar_admin():
    if current_user.usertype == 1:
        Correo=request.form['Correo']
        Nombre=request.form['Nombre']
        user=current_user.id
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(UserId) as exist FROM users where UserId!={} and Email='{}'".format(user,Correo)
        cur.execute(query)
        programming = cur.fetchall()
        for lista in programming:
            exist=lista['exist']
        
        if int(exist) > 0:
            mens='Este correo ya exite'
        else:
            cur = mysql.connection.cursor()
            cur.execute( "UPDATE users set Nombre=%s, Email=%s WHERE UserId= %s", (Nombre,Correo,user))
            mysql.connection.commit()
            mens="Datos actulizados con exito"
        
        flash(mens)

        
        return redirect(url_for("datos_admin"))
    else:
        if current_user.usertype == 3:
            Correo=request.form['Correo']
            Nombre=request.form['Nombre']
            user=request.form['UserId']
            Activo=request.form['Activo']

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT COUNT(UserId) as exist FROM users where UserId!={} and Email='{}'".format(user,Correo)
            cur.execute(query)
            programming = cur.fetchall()
            for lista in programming:
                exist=lista['exist']
            
            if int(exist) > 0:
                mens='Este correo ya exite'
            else:
                cur = mysql.connection.cursor()
                cur.execute( "UPDATE users set Nombre=%s, Email=%s, Activo=%s WHERE UserId= %s", (Nombre,Correo,Activo,user))
                mysql.connection.commit()
                mens="Datos actulizados con exito"
            flash(mens)    
            #return admin_edit(user) ,id=user
            return redirect(url_for("admin_edit",id=user))
        else:
            return logout()
#cambiar contra admin--------------------------------------------------------------------------------------------------
@app.route('/contra_admin',methods=["POST","GET"])
@login_required
def contra_admin():
    email_content = """
        <html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

            <title>ASEBEP</title>
        </head>

        <body>


            <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4">
                <tr>
                    <td>
                        
                        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
                            <tr>
                                <td>
                                    <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                                        <tr>
                                            <td width="570" align="center" bgcolor="#cda434">
                                                <h1>Combio de Contraseña</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td width="570" align="left" bgcolor="#cda434">
                                                <p>Usted cambio la Contraseña de su cuenta en la plataforma ASEBEP UNAH-VS</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="150" valign="top" bgcolor="d0d0d0" >
                                                <img src="https://asebepunahcu.files.wordpress.com/2017/09/logo-asebep.png?w=294" width="150"height="150" />
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td width="200" valign="top">
                                                <h3 align="center"><b>ASEBEP UNAH-VS</b></h3>
                                                <br><b>Ustes cambio su contraseña en la plataforma ASEBEP</b> </br>
                                            </td>
                                            
                                        </tr>
                                    </table>
                                </td>
                            </tr>


                        </table>
                        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
                            <tr>
                                <td bgcolor="#40CFFF" align="center">
                                    <p id="bajo">Diseñado para una mejor experiencia de nuestros Usuarios</p>
                                    <p ><a href="https://www.facebook.com/Asebep-Unah-Vs-101545674954541">Facebook ASEBEP</a> | <a href="https://www.instagram.com/asebepvs/">Instagram ASEBEP</a> </p>
                                </td>
                            </tr>
                        </table><!-- top message -->
                    </td>
                </tr>
            </table><!-- wrapper -->

        </body>

        </html>
        
        """
    if current_user.usertype == 1:
        contra=request.form['NC']
        password=request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user=current_user.id
        query = "SELECT password,Email FROM users where UserId={} ".format(user,)
        cur.execute(query)
        programming = cur.fetchall()
        for lista in programming:
            base=lista['password']
            Correo=lista['Email']

        if check_password_hash(base, password):
            Npassword=generate_password_hash(contra)
            cur = mysql.connection.cursor()
            cur.execute( "UPDATE users set password=%s WHERE UserId= %s", (Npassword,user))
            mysql.connection.commit()
            flash('Contraseña actulizada con exito')
            msg = email.message.Message()
            msg['Subject'] = 'Cambio de Contraseña'
            msg['From'] = 'asabepunahvs@gmail.com'
            msg['To'] = Correo
            password = "Ae$Tb5Waf3EEq"
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8').strip())
        else:
            flash('La contraseña actual es incorrecta')
        #return datos_admin()
        return redirect(url_for("datos_admin"))
    else:
        if current_user.usertype == 2:
            contra=request.form['NC']
            password=request.form['password']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            user=current_user.id
            query = "SELECT password,Email FROM users where UserId={} ".format(user,)
            cur.execute(query)
            programming = cur.fetchall()
            for lista in programming:
                base=lista['password']
                Correo=lista['Email']

            if check_password_hash(base, password):
                Npassword=generate_password_hash(contra)
                cur = mysql.connection.cursor()
                cur.execute( "UPDATE users set password=%s WHERE UserId= %s", (Npassword,user))
                mysql.connection.commit()
                flash('Contraseña actulizada con exito')
  
                msg = email.message.Message()
                msg['Subject'] = 'Cambio de Contraseña'
                msg['From'] = 'asabepunahvs@gmail.com'
                msg['To'] = Correo
                password = "Ae$Tb5Waf3EEq"
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()
                # Login Credentials for sending the mail
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8').strip())
            else:
                flash('La contraseña actual es incorrecta')
            #return Mis_Datos()
            return redirect(url_for("Mis_Datos"))
        else:
            return logout()

#-------------------------------------------------------Mantenimiento-------------------------------------------------------------------#
@app.route('/Mantenimiento')
@login_required
def Mantenimiento(): 
    if current_user.usertype == 1: 
        return render_template("admin/Mantenimiento.html")
    else:
        return logout()

#agregar nueva carrera----------------------------------------------------------------------
@app.route('/Agregar_Carrera',methods=["POST","GET"])
@login_required
def Agregar_Carrera(): 
    if current_user.usertype == 1: 
        Carrera=request.form['Carrera']
        if(Carrera==''):
            flash('Error: debe de llenar el campo')
        else:
            cur = mysql.connection.cursor()
            cur.execute( "INSERT INTO carrera(Carrera) VALUES (%s)", (Carrera,))
            mysql.connection.commit()
            flash('Carrera Agregada con exito')
        
        return redirect(url_for('Mantenimiento'))
    else:
        return logout()
#agregar nueva Beca----------------------------------------------------------------------
@app.route('/Agregar_Beca',methods=["POST","GET"])
@login_required
def Agregar_Beca(): 
    if current_user.usertype == 1: 
        Beca=request.form['Beca']
        if(Beca==''):
            flash('Error: debe de llenar el campo')
        else:
            cur = mysql.connection.cursor()
            cur.execute( "INSERT INTO beca(Tipo) VALUES (%s)", (Beca,))
            mysql.connection.commit()
            flash('Tipo de Beca Agregada con exito')
        
        return redirect(url_for('Mantenimiento'))
    else:
        return logout()


#==============================================================================Elementos Estudiantes====================================================================#

#---------------------------------------------------------------------------Elementos Index-----------------------------------------------------------------------------#
#ruta inicio Estudiantes-----------------------------------------------------------------------------------------------------
@app.route('/InicioEstudiante')
@login_required
def homeEstudiante():  
    if current_user.usertype == 2:
        return render_template("user/index_estudiantes.html")
    else:
        return logout()

#llamar a tabla usuario estudiante-------------------------------------------------------------------------------------------
@app.route("/Mis_Actividades",methods=["POST","GET"])
@login_required
def Mis_Actividades():
    if current_user.usertype == 2:
        if request.method == 'POST':
            Codigo = current_user.eid
            mes = request.form['mes']   
            ano=request.form['ano']
            if(mes=='0' and ano=='0'):
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = """SELECT * FROM view_registroestudiantes WHERE EstudiantesId='{}' 
                and MONTH(Fecha)=MONTH(CURRENT_DATE()) 
                and Year(Fecha)=Year(CURRENT_DATE()) ORDER by Fecha,Hora_I ASC""".format(Codigo)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('comp_user/Mis_Actividades.html', programming=programming)})
            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = """SELECT * FROM view_registroestudiantes 
                WHERE EstudiantesId='{}' 
                and MONTH(Fecha)='{}' 
                and Year(Fecha)='{}' ORDER by Fecha,Hora_I ASC""".format(Codigo,mes,ano)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('comp_user/Mis_Actividades.html', programming=programming)}) 
    else:
        return logout() 

#llamar Hora registro estudiante---------------------------------------------------------------------------------------------------------------------------------------
@app.route("/Total_Horas",methods=["POST","GET"])
@login_required
def Horas():
    if current_user.usertype == 2:
            Codigo = current_user.eid
            mes = request.form['mes']
            ano=request.form['ano']
            if(mes=='0' and ano=='0'):
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT sum(Horas) as Horas FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)=MONTH(CURRENT_DATE()) and Year(Fecha)=Year(CURRENT_DATE())".format(Codigo)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('complementos/Horas.html', programming=programming)})

            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT sum(Horas) as Horas FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)='{}' and Year(Fecha)='{}'".format(Codigo,mes,ano)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('complementos/Horas.html', programming=programming)})
    else:
            Codigo = request.form['EstudiantesId']
            mes = request.form['mes']
            ano=request.form['ano']
            if(mes=='0' and ano=='0'):
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT sum(Horas) as Horas FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)=MONTH(CURRENT_DATE()) and Year(Fecha)=Year(CURRENT_DATE())".format(Codigo)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('complementos/Horas.html', programming=programming)})

            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "SELECT sum(Horas) as Horas FROM view_registroestudiantes WHERE EstudiantesId='{}' and MONTH(Fecha)='{}' and Year(Fecha)='{}'".format(Codigo,mes,ano)
                cur.execute(query)
                programming = cur.fetchall()
                return jsonify({'data': render_template('complementos/Horas.html', programming=programming)})
    
    

#Editar Actividad usuario estudiante-----------------------------------------------------------------------------------------------------
@app.route('/Estudiante_Actividadedit/<id>/<ide>', methods=['POST','GET'])
@login_required
def get_actividadestudiante(id,ide):
    if current_user.usertype == 2:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM view_registroestudiantes WHERE idActividades= %s and EstudiantesId= %s", (id,ide))
        mysql.connection.commit()
        Lista = cur.fetchall()
        cur.close()
        for lista in Lista:
            Horaf=lista['Hora_F']
            HoraI=lista['Hora_I']

        hora1 = datetime.strptime(str(HoraI), "%X").time()
        hora2 = datetime.strptime(str(Horaf), "%X").time()

        if(hora1 < datetime.strptime("10:00:00", "%X").time()):
            HoraI="0"+str(HoraI)

        if(hora2 < datetime.strptime("10:00:00", "%X").time()):
            Horaf="0"+str(Horaf)

        for lista in Lista:
            lista['Hora_F']=Horaf
            lista['Hora_I']=HoraI
        
        return render_template('user/Estudiante_ActividadEdit.html',Actividades=Lista)
    else:
        return logout()

#Eliminar evidencia --------------------------------------------------------------------------------------------------
@app.route('/Eliminar_Evidencia/<idr>/<ida>',methods=["POST","GET"])
@login_required
def Eliminar_Evidencia(idr,ida):
    if current_user.usertype == 2:
        ide=current_user.eid
        cur = mysql.connection.cursor()
        cur.execute( "UPDATE registro set Evidencia='' WHERE RegistroId= %s", (idr,))
        mysql.connection.commit()
        flash('Evidencia Eliminada......')
        #return get_actividadestudiante(ida,ide)
        return redirect(url_for("get_actividadestudiante",id=ida,ide=ide))
    else:
        return logout()
    
#Eliminar Mi Actividad------------------------------------------------------------------------------------------------------------
@app.route("/Eliminar_MiActiva",methods=["POST","GET"])
@login_required
def Eliminar_MiActiva():
    if request.method == 'POST':
        id = request.form['idActividad']
        idr = request.form['RegistroId']

        cur = mysql.connection.cursor()
        cur.execute("delete from registro WHERE RegistroId=%s",(idr,))
        mysql.connection.commit()
        
        cur1 = mysql.connection.cursor()
        cur1.execute("UPDATE actividades SET Inscritos = Inscritos - 1  WHERE idActividades=%s", (id,))
        mysql.connection.commit()
        flash('La Actividad ha sido eliminada con exito')

        #return homeEstudiante()
        return redirect(url_for("homeEstudiante"))

#subir evidencia de actividad---------------------------------------------------------------------------------------------------
@app.route("/upload/<idr>/<aid>", methods=['POST'])
@login_required
def uploader(idr,aid):
    if request.method == 'POST':
        # obtenemos el archivo del input "archivo"
        filename = request.form['archivo']
        cur = mysql.connection.cursor()
        cur.execute( "UPDATE registro set Evidencia=%s WHERE RegistroId= %s", (filename,idr))
        mysql.connection.commit()
        flash('Evidencia Subida con exito......')
        return redirect(url_for("get_actividadestudiante",id=aid,ide=current_user.eid))

#---------------------------------------------------------------Actividades Disponibles-------------------------------------------------#
#Actividad Disponibles
@app.route("/Actividades_Disponibles")
@login_required
def Actividades_Disponibles():
    if current_user.usertype == 2:    
        return render_template('user/Actividades_Estudiante.html')
    else:
        return logout()
#llenar tabla actividades--------------------------------------------------------------------------------------------------------
@app.route("/LlenarActividades",methods=["POST","GET"])
@login_required
def LlenarActividades():   
    
        #and day(Fecha)>= Day(curdate()) ORDER by Fecha,Hora_I ASC
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """SELECT * FROM actividades 
        where MONTH(Fecha)=MONTH(CURRENT_DATE()) 
        and Year(Fecha)=Year(CURRENT_DATE())
        and day(Fecha)>= Day(curdate()) ORDER by Fecha,Hora_I ASC"""
        cur.execute(query)
        programming = cur.fetchall()
        print('estoy aqui: ',programming)
        return jsonify({'data': render_template('comp_user/Llenar_Actividades.html', listas=programming)})

#Editar Inscribirse en Actividad-------------------------------------------------------------------------------------------------------
@app.route('/Estudiante_Inscripcion/<id>', methods=['POST','GET'])
@login_required
def Estudiante_Inscripcion(id):
    if current_user.usertype == 2: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM actividades WHERE idActividades= %s ", (id,))
        mysql.connection.commit()
        Lista = cur.fetchall()
        cur.close()
        for lista in Lista:
            Horaf=lista['Hora_F']
            HoraI=lista['Hora_I']

        hora1 = datetime.strptime(str(HoraI), "%X").time()
        hora2 = datetime.strptime(str(Horaf), "%X").time()

        if(hora1 < datetime.strptime("10:00:00", "%X").time()):
            HoraI="0"+str(HoraI)

        if(hora2 < datetime.strptime("10:00:00", "%X").time()):
            Horaf="0"+str(Horaf)

        for lista in Lista:
            lista['Hora_F']=Horaf
            lista['Hora_I']=HoraI

        return render_template('user/Estudiante_Inscripcion.html',Actividades=Lista)
    else:
        return logout()

#Comprobar se si puede inscribir----------------------------------------------------------- 
@app.route("/Comprobar",methods=["POST","GET"])
def Comprobar():
    if request.method == 'POST':
        ide = current_user.eid
        codigo= request.form['idActividad']
        nivel=0
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "select COUNT(EstudiantesId) as count from registro where idActividades='{}' and EstudiantesId='{}'".format(codigo,ide)
        cur.execute(query)
        programming = cur.fetchall()
        for p in programming:
            exis=p['count']

        if exis==0 :
            nivel=1
            
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT (Cupos-Inscritos) as Cupos from actividades WHERE idActividades='{}'".format(codigo)
            cur.execute(query)
            programming = cur.fetchall()
            for p in programming:
                cupos=p['Cupos']

            if int(cupos)>0:
                nivel=2
                Lista=[nivel,ide,codigo]
                return jsonify({'data': render_template('comp_user/comprobar_actividad.html',Comprobar=Lista)})
            else:
                Lista=[nivel,ide,codigo]
                return jsonify({'data': render_template('comp_user/comprobar_actividad.html',Comprobar=Lista)})
            
            
        else:
            Lista=[nivel,ide,codigo]
            return jsonify({'data': render_template('comp_user/comprobar_actividad.html',Comprobar=Lista)})

#registrar mi cuenta-------------------------------------------------------------------------------------------------------
@app.route("/Registrarme/<codigo>/<id>",methods=["POST","GET"])
@login_required
def Registrarme(codigo,id):
        cursor = mysql.connection.cursor()
        sql = "SELECT *from registro where idActividades={} and EstudiantesId={} ".format(codigo,id)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row != None:
            flash('Te has inscrito en esta actividad')   
            
            return redirect(url_for("Estudiante_Inscripcion",id=codigo))
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT (Cupos-Inscritos) as Cupos from actividades WHERE idActividades='{}'".format(codigo)
            cur.execute(query)
            programming = cur.fetchall()
            for p in programming:
                cupos=p['Cupos']

            if int(cupos)>0:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO registro (idActividades, EstudiantesId,Evidencia) VALUES (%s,%s,'')", (codigo,id))
                mysql.connection.commit()
                cur1 = mysql.connection.cursor()
                cur1.execute("UPDATE actividades SET Inscritos = Inscritos + 1  WHERE idActividades=%s", (codigo,))
                mysql.connection.commit()
                flash('Te has inscrito en esta actividad')
                return redirect(url_for("Estudiante_Inscripcion",id=codigo))
            else:
                flash('No hay cupos para esta actividad')
                return redirect(url_for("Estudiante_Inscripcion",id=codigo))



#-------------------------------------------------------------------------------Mis Datos-----------------------------------------------------------------------------#
@app.route('/Mis_Datos')
@login_required
def Mis_Datos():
    if current_user.usertype == 2: 
        id = current_user.eid
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM view_estudiantes where EstudiantesId={}".format(id)
        cur.execute(query)
        programming = cur.fetchall()
            
        return render_template("user/Mis_Datos.html",listas=programming)



#Actualizar MisDatos--------------------------------------------------------------------------------------------------------------------------------
@app.route("/Actualizar_MisDatos",methods=["POST","GET"])
def Actualizar_MisDatos():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Cuenta = request.form['Cuenta']
        Telefono = request.form['Telefono']
        Correo = request.form['Correo']
        BecaId = request.form['Beca']
        CarreraId = request.form['Carrera']
        EstudiantesId = current_user.eid
        user=current_user.id
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(UserId) as exist FROM users where UserId!={} and Email='{}'".format(user,Correo)
        cur.execute(query)
        programming = cur.fetchall()
        for lista in programming:
            exist=lista['exist']
        
        if int(exist) > 0:
            mens='Este correo ya exite'
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT COUNT(UserId) as exist FROM estudiantes where UserId!={} and NCuenta='{}'".format(user,Cuenta)
            cur.execute(query)
            programming = cur.fetchall()
            for lista in programming:
                exist=lista['exist']
            
            if int(exist) > 0:
                mens='Esta cuenta ya exite'
            else:
                cur = mysql.connection.cursor()
                cur.execute( "UPDATE users set Nombre=%s, Email=%s WHERE UserId= %s", (Nombre,Correo,user))
                mysql.connection.commit()
                cur1 = mysql.connection.cursor()
                cur1.execute("UPDATE estudiantes SET NCuenta=%s,BecaId=%s,CarreraId=%s,Telefono=%s WHERE EstudiantesId=%s",(Cuenta,BecaId,CarreraId,Telefono,EstudiantesId))
                mysql.connection.commit()
                mens="Datos actulizados con exito"

        flash(mens)
        return redirect(url_for("Mis_Datos"))

#ver y subir informes-----------------------------------------------------------------------------------------------------------
@app.route('/Mis_Informes')
@login_required
def Mis_Informes():
    if current_user.usertype == 2: 
        return render_template('user/Mis_Informes.html')
#-------------------------------pestana subir informe---------------------------------------------------------------------------------
@app.route('/Subir_Informes')
@login_required
def Subir_Informes():
    if current_user.usertype == 2: 
        return render_template('user/Subir_Informes.html')

#-----------------------------------subir informe-------------------------------------------------------------------------------------------
@app.route("/uploadInforme", methods=["POST","GET"])
@login_required
def uploadInforme():
    app.config['UPLOAD_FOLDER'] = './src/static/Reportes'

    if request.method == 'POST':
        # obtenemos el archivo del input "archivo"
        filename = request.form['archivo']
        ano = request.form['ano']
        mes = request.form['mes']
        ide=current_user.eid
        desc=printMonth(int(mes),ano)
        cur = mysql.connection.cursor()
        cur.execute( "INSERT INTO `informes`(EstudiantesId,Fecha,ano,Descripcion,Reporte) VALUES (%s,CURRENT_DATE(),%s,%s,%s)", (ide,ano,desc,filename))
        mysql.connection.commit()
        flash('Informe Subido con exito......')
        return redirect(url_for('Mis_Informes'))

def printMonth(num,ano):
    if num == 1:      
        month ='Informe de Enero del '+ano
    elif num == 2:
        month = 'Informe de Febrero del '+ano
    elif num == 3:
        month = 'Informe de Marzo del '+ano
    elif num == 4:
        month= 'Informe de Abril del '+ano
    elif num == 5:
        month= 'Informe de Mayo del '+ano
    elif num == 6:
        month = 'Informe de Junio del '+ano
    elif num == 7:
        month = 'Informe de Julio del '+ano
    elif num == 8:
        month = 'Informe de Agosto del '+ano
    elif num == 9:
        month= 'Informe de Septiembre del '+ano
    elif num == 10:
        month= 'Informe de Octubre del '+ano
    elif num == 11:
        month= 'Informe de Noviembre del '+ano
    elif num == 12:
        month= 'Informe de Diciembre del '+ano
    return month

#----------------------------------------------------------------Mis Reclamos--------------------------------------------------------#
#Llnar Mis reclamos----------------------------------------------------------------------------------------------------------------------------
@app.route("/Llenar_Reclamos",methods=["POST","GET"])
@login_required
def Llenar_Reclamos():
    if current_user.usertype == 2:
        if request.method == 'POST':  
            eid=current_user.eid
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM reclamos where EstudiantesId={} ORDER by Fecha ASC".format(eid,)
            cur.execute(query)
            programming = cur.fetchall()
    
            return jsonify({'data': render_template('comp_user/bandeja_reclamos.html', listas=programming)})
    else:
        return logout()
#Pagina Mis Reclamos--------------------------------------------------------------------------------------------------------
@app.route("/Mis_Reclamos",methods=["POST","GET"])
@login_required
def Mis_Reclamos():
    if current_user.usertype == 2:
        return render_template('user/Mis_Reclamos.html')
    else:
        return logout()

#Hacer Reclamo-------------------------------------------------------------------------------------------------------------
@app.route("/hacer_reclamo",methods=["POST","GET"])
@login_required
def hacer_reclamo():
    if current_user.usertype == 2:
        eid=current_user.eid
        reclamo = request.form['reclamo']
        cur = mysql.connection.cursor()
        cur.execute( "INSERT INTO reclamos(EstudiantesId,Descripcion,Fecha,Visto) VALUES (%s,%s,CURRENT_DATE(),'NO')", (eid,reclamo))
        mysql.connection.commit()
        flash('Se envio su reclamo')
        return redirect(url_for('Mis_Reclamos'))


# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
    csrf.init_app(app)
    app.run()