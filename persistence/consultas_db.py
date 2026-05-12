from mysql.connector import Error
from persistence.db import get_connection



# 1. METODO DE REGISTRO DE CLIENTE
def registrar_cliente(nombre, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO clientes (nombre, email) VALUES (%s, %s)"
        cursor.execute(query, (nombre, email))
        conn.commit()
        return {"status": "success", "message": f"Cliente '{nombre}' registrado con ID {cursor.lastrowid}"}
    except Error as e:
        return {"status": "error", "message": f"Fallo al registrar cliente: {e.msg}"}
    finally:
        cursor.close()
        conn.close()



# 2. METODO CON TRANSACCION
def realizar_venta(cliente_id, producto_id, cantidad, precio_unitario):
    """
    Este método cumple con START TRANSACTION, COMMIT y ROLLBACK.
    No necesita lógica de stock aquí porque los TRIGGERS:
    - 'validar_stock' detendrá la inserción si no hay suficiente.
    - 'descontar_stock' restará la cantidad automáticamente al insertar.
    """
    conn = get_connection()
    cursor = conn.cursor()
    total = cantidad * precio_unitario
    
    try:
        cursor.execute("START TRANSACTION;")
        
        # Inserta la Orden
        query_orden = "INSERT INTO ordenes (cliente_id, usuario_id, total) VALUES (%s, %s, %s)"
        cursor.execute(query_orden, (cliente_id, 2, total))
        orden_id = cursor.lastrowid
        
        # Inserta el Detalle
        # Al ejecutar esto, MySQL ejecuta automáticamente el TRIGGER 'descontar_stock'
        query_detalle = "INSERT INTO orden_productos (orden_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_detalle, (orden_id, producto_id, cantidad, precio_unitario))
        
        # Registra el Pago
        query_pago = "INSERT INTO pagos (orden_id, monto, metodo_pago) VALUES (%s, %s, 'efectivo')"
        cursor.execute(query_pago, (orden_id, total))
        
        conn.commit()
        return {"status": "success", "message": f"Venta #{orden_id} completada (Stock actualizado por Trigger)"}
        
    except Error as e:
        # Si el TRIGGER 'validar_stock' lanza un SIGNAL SQLSTATE, el error caerá aquí
        conn.rollback()
        return {"status": "error", "message": f"Fallo en la operación: {e.msg}"}
    finally:
        cursor.close()
        conn.close()



# 3. REPORTE CON VISTA (Requisito: VIEW)
def consultar_inventario():
    conn = get_connection()
    cursor = conn.cursor()
    # Llamamos a una de las vistas creadas
    cursor.execute("SELECT * FROM vista_productos_calidad")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return resultados



# 4. REPORTE COMPLEJO (Requisito: GROUP BY, HAVING, ORDER BY)
def reporte_ventas_por_cliente():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT c.nombre, COUNT(o.id) as num_ordenes, SUM(o.total) as total_gastado
        FROM clientes c
        JOIN ordenes o ON c.id = o.cliente_id
        GROUP BY c.nombre
        HAVING total_gastado > 0
        ORDER BY total_gastado DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return resultados



# 5. CONSULTA AVANZADA (Requisito: JOIN, LIKE)
def filtrar_clientes_por_nombre(nombre_buscar):
    conn = get_connection()
    cursor = conn.cursor()
    # Ejemplo de LIKE
    query = "SELECT * FROM clientes WHERE nombre LIKE %s"
    cursor.execute(query, (f"%{nombre_buscar}%",))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return resultados
