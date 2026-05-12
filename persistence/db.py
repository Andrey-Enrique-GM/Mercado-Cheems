import pymysql

def get_connection():
    return pymysql.connect(
        host="34.30.245.236",
        port=3306,
        user="000",
        password="000",
        database="db_sistema_ventas"
    )