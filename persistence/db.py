import pymysql

def get_connection():
    return pymysql.connect(
        host="jdbc:mysql://34.30.245.236:3306/db_sistema_ventas",
        user="---",
        password="---",
        database="db_sistema_ventas",
        port=3306
    )