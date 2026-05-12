from flask import Flask, render_template, jsonify, request
from persistence.consultas_db import (
    registrar_cliente, 
    realizar_venta, 
    consultar_inventario, 
    reporte_ventas_por_cliente,
    filtrar_clientes_por_nombre
)


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
    return render_template('welcome.html')



# --- RUTAS DE API ---

@app.route('/api/login', methods=['POST'])
def api_login():
    return jsonify({'success': True})


@app.route('/api/inventario')
def api_inventario():
    # Llama al Método 3: VIEW
    datos = consultar_inventario()
    return jsonify(datos)


@app.route('/api/reporte-ventas')
def api_reporte_ventas():
    # Llama al Método 4: GROUP BY/HAVING
    datos = reporte_ventas_por_cliente()
    return jsonify(datos)


@app.route('/api/realizar-venta', methods=['POST'])
def api_realizar_venta():
    # Llama al Método 2: TRANSACTION + TRIGGERS
    data = request.json
    resultado = realizar_venta(
        cliente_id=data['cliente_id'],
        producto_id=data['producto_id'],
        cantidad=int(data['cantidad']),
        precio_unitario=float(data['precio'])
    )
    return jsonify(resultado)


@app.route('/api/registrar-cliente', methods=['POST'])
def api_registrar_cliente():
    # Llama al Método 1: INSERT simple
    data = request.json
    resultado = registrar_cliente(data['nombre'], data['email'])
    return jsonify(resultado)


@app.route('/api/buscar-cliente')
def api_buscar_cliente():
    # Llama al Método 5: JOIN + LIKE
    nombre = request.args.get('nombre', '')
    resultado = filtrar_clientes_por_nombre(nombre)
    return jsonify(resultado)



if __name__ == '__main__':
    app.run()
