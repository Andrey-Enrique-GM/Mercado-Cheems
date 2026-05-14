import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="--",
        password="--",
        database="db_sistema_ventas"
    )