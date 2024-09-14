import pymysql
from flask import Flask, jsonify, render_template, request
#from dbconfig import mysql
#from flaskext.mysql import MySQL
#from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='Pasw75:v',
                                db='flaskapp')

#mysql = obtener_conexion()
@app.route('/')
def main():
    #return "Hola Mundo"
    return render_template('index.html')
@app.route('/envio')
def enviar():
    #print(request)
    #print(request.args)
    connection =None
    cursor= None
    try:
        data = request.args
        #connection = mysql.connect()
        connection= obtener_conexion()
        if(connection==None):
            return "Conexion fallida"
        cursor = connection.cursor()
        nombre = data['name']
        telefono = data['phone']
        email = data['email']
        resumen = data['sumary']
        direcc = data['dire']
        insert_query = """
            INSERT INTO usuario (name, email, phone, dire, sumary)
            VALUES (%s, %s, %s, %s, %s)
            """
        with connection.cursor() as cursor:
            cursor.execute(insert_query, ( nombre, email, telefono, direcc, resumen))
        connection.commit()
        connection.close()
        #cursor.execute(insert_query, ( nombre, email, telefono, direcc, resumen))
        print("waza?")
        #cursor.close()
        #connection.close()
        return "Ok"
    except Exception as ex:
        return jsonify({'error': str(ex)}), 400
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)