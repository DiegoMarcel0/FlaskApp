from dbconfig import obtener_conexion
from flask import Flask, jsonify, redirect, render_template, request, url_for
#from dbconfig import mysql
#from flaskext.mysql import MySQL
#from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

@app.route('/')
def main():
    #return "Hola Mundo"
    return redirect(url_for('datos'))

@app.route('/datos')
def datos():
    connection= None
    data = None
    try:
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        sql = "SELECT ID, name, email, sumary FROM usuario"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
        connection.close()
        #print(data)
        #return jsonify(data)
    except Exception as e:
        print(e)
    return render_template('datos.html', data = data)

@app.route("/editar/<int:id>")
def editar(id):
    connection= None
    data = None
    try:
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        sql = "SELECT * FROM usuario WHERE ID= %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
            data = cursor.fetchall()
        print(data)
        connection.close()
    except Exception as e:
        print(e)
        
    return render_template("editar.html", tupla = data)



@app.route('/insertar')
def insertar():
    return render_template('insertar.html')

@app.route('/envio', methods = ["POST","GET"])
def enviar():
    #print(request)
    #print(request.args)
    connection =None
    cursor= None
    try:
        if request.method != "POST":
            return "Error: Metodo NO POST"
        #connection = mysql.connect()
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        nombre = request.form['name']
        telefono = request.form['phone']
        email = request.form['email']
        resumen = request.form['sumary']
        direcc = request.form['dire']
        insert_query = """
            INSERT INTO usuario (name, email, phone, dire, sumary)
            VALUES (%s, %s, %s, %s, %s)
            """
        with connection.cursor() as cursor:
            cursor.execute(insert_query, ( nombre, email, telefono, direcc, resumen))
        connection.commit()
        connection.close()
        #print("waza?")
        
    except Exception as e:
        print(e)
    return "Exito"
    #print("Enviado Correctamente")
    #return render_template("datos.html")
@app.route('/update', methods = ["POST","GET"])
def actualizar():
    #print(request)
    #print(request.args)
    connection =None
    cursor= None
    try:
        if request.method != "POST":
            return "Error: Metodo NO POST"
        #connection = mysql.connect()
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        id = request.form['id']
        ID= int(id)
        nombre = request.form['name']
        telefono = request.form['phone']
        email = request.form['email']
        resumen = request.form['sumary']
        direcc = request.form['dire']
        insert_query = """
            UPDATE usuario
            SET name = %s, email = %s, phone=%s, dire=%s, sumary=%s
            WHERE ID=%s
            """
        with connection.cursor() as cursor:
            cursor.execute(insert_query, ( nombre, email, telefono, direcc, resumen, ID))
        connection.commit()
        connection.close()
        #print("waza?")
        
    except Exception as e:
        print(e)
    return "Exito"

@app.route('/delete/<int:id>')
def delete(id):
    connection= None
    try:
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        sql = "DELETE FROM usuario WHERE ID= %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
            connection.commit()
        connection.close()
    except Exception as e:
        print(e)
    return "exito"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#url_for usa los nombres de las funciones