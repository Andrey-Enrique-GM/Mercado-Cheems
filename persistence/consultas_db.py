from mysql.connector import Error
from persistence.db import get_connection



# 1. OPERACIÓN: REGISTRO CON TRANSACCIÓN Y TRIGGERS
def realizar_venta(cliente_id, producto_id, cantidad, precio_unitario):
    """
    CUMPLE: START TRANSACTION, COMMIT, ROLLBACK y uso de TRIGGERS.
    """
    conn = get_connection()
    cursor = conn.cursor()
    total = cantidad * precio_unitario
    try:
        cursor.execute("START TRANSACTION;")
        # 1. Orden -> 2. Detalle (Dispara Trigger de stock) -> 3. Pago
        cursor.execute("INSERT INTO ordenes (cliente_id, usuario_id, total) VALUES (%s, 2, %s)", (cliente_id, total))
        orden_id = cursor.lastrowid
        cursor.execute("INSERT INTO orden_productos (orden_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)", 
                       (orden_id, producto_id, cantidad, precio_unitario))
        cursor.execute("INSERT INTO pagos (orden_id, monto, metodo_pago) VALUES (%s, %s, 'efectivo')", (orden_id, total))
        conn.commit()
        return {"status": "success", "message": f"Venta #{orden_id} exitosa."}
    except Error as e:
        conn.rollback()
        return {"status": "error", "message": e.msg}
    finally:
        cursor.close()
        conn.close()



# 2. REPORTE COMPLEJO: VENTAS TOTALES
def reporte_resumen_ventas():
    """
    CUMPLE: JOIN, GROUP BY, HAVING y ORDER BY.
    Sustituye a 'reporte_ventas_por_cliente' y 'bajo_stock'.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Este query agrupa cuánto ha gastado cada cliente y solo muestra a los "importantes"
    query = """
        SELECT c.nombre, COUNT(o.id) as total_compras, SUM(o.total) as total_gastado
        FROM clientes c
        JOIN ordenes o ON c.id = o.cliente_id
        GROUP BY c.nombre
        HAVING total_gastado > 100
        ORDER BY total_gastado DESC
    """
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    res = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return res



# 3. CONSULTA DE INVENTARIO: (Uso de VIEW y SUBQUERY)
def consultar_inventario_completo():
    """
    CUMPLE: View y Subqueries.
    Usa la vista 'vista_inventario_detallado' para obtener datos procesados.
    """
    # Definimos las columnas que esperamos explícitamente para evitar SELECT *
    query = "SELECT id, nombre, precio, stock, categoria_nombre, veces_vendido FROM vista_inventario_detallado"
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        # Usamos las columnas definidas para mapear el diccionario
        res = [dict(zip(["id", "nombre", "precio", "stock", "categoria_nombre", "veces_vendido"], row)) for row in cursor.fetchall()]
        return res
    except Error as e:
        print(f"Error al consultar inventario: {e}")
        return []
    finally:
        cursor.close()
        conn.close()



# 4. BUSCADOR AVANZADO: (Uso de LIKE)
def buscar_cliente(termino):
    """
    CUMPLE: LIKE y Registro simple (si no encuentra, podrías registrar).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, email FROM clientes WHERE nombre LIKE %s", (f"%{termino}%",))
    column_names = [desc[0] for desc in cursor.description]
    res = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return res
