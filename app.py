from flask import Flask, redirect, render_template, jsonify, request
from persistence.consultas_db import *


app = Flask(__name__)

# --- RUTAS DE NAVEGACION ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    clientes = obtener_clientes()
    productos = obtener_productos()
    return render_template(
        'welcome.html',
        clientes=clientes,
        productos=productos
    )


# --- RUTAS DE API ---
@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():

    cliente_id = request.form['id_cliente']
    producto_id = request.form['id_producto']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    resultado = realizar_venta(
        cliente_id,
        producto_id,
        int(cantidad),
        float(precio)
    )

    clientes = obtener_clientes()
    productos = obtener_productos()

    return render_template(
        'welcome.html',
        clientes=clientes,
        productos=productos,
        resultado=resultado
    )

@app.route('/api/login', methods=['POST'])
def api_login():
    return jsonify({'success': True})


@app.route('/api/inventario-completo')
def api_inventario_completo():
    # Consulta de inventario completo con VIEW y subqueries
    datos = consultar_inventario_completo()
    return jsonify(datos)


@app.route('/api/reporte-resumen-ventas')
def api_reporte_resumen_ventas():
    # Reporte complejo con JOIN, GROUP BY, HAVING y ORDER BY
    datos = reporte_resumen_ventas()
    return jsonify(datos)


@app.route('/api/realizar-venta', methods=['POST'])
def api_realizar_venta():
    # Operación con transacción y triggers
    data = request.json
    resultado = realizar_venta(
        cliente_id=data['cliente_id'],
        producto_id=data['producto_id'],
        cantidad=int(data['cantidad']),
        precio_unitario=float(data['precio'])
    )
    return jsonify(resultado)


@app.route('/api/buscar-cliente')
def api_buscar_cliente():
    # Búsqueda avanzada con LIKE
    termino = request.args.get('termino', '')
    resultado = buscar_cliente(termino)
    return jsonify(resultado)

@app.route('/api/clientes')
def api_clientes():

    clientes = obtener_clientes()

    return jsonify(clientes)

@app.route('/api/producto/<int:producto_id>')
def api_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if producto:
        return jsonify(producto)
    return jsonify({
        "error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run()
    