/**
 * MERCADO CHEEMS - Lógica de Dashboard y Persistencia
 * Conecta los botones del menú con los métodos de Python/MySQL
 */

const contenedor = document.getElementById('contenedor-principal');



// 1. FUNCIÓN PARA MOSTRAR EL REPORTE DE VENTAS (MÉTODO 4: GROUP BY/HAVING)
function verReporteVentas() {
    fetch('/api/reporte-ventas')
        .then(res => res.json())
        .then(data => {
            let html = `
                <h3>Ranking de Clientes Top</h3>
                <p class="text-muted">Clientes con compras mayores a $0 (Uso de HAVING y GROUP BY)</p>
                <table class="table table-dark table-striped">
                    <thead>
                        <tr><th>Cliente</th><th># Ordenes</th><th>Total Gastado</th></tr>
                    </thead>
                    <tbody>`;
            data.forEach(r => {
                html += `<tr><td>${r.nombre}</td><td>${r.num_ordenes}</td><td>$${r.total_gastado}</td></tr>`;
            });
            html += `</tbody></table>`;
            contenedor.innerHTML = html;
        });
}



// 2. FUNCIÓN PARA CONSULTAR INVENTARIO (MÉTODO 3: VIEW)
function verInventario() {
    fetch('/api/inventario')
        .then(res => res.json())
        .then(data => {
            let html = `
                <h3>Inventario Actual</h3>
                <p class="text-muted">Datos obtenidos desde la VISTA: vista_productos_calidad</p>
                <div class="row">`;
            data.forEach(p => {
                html += `
                    <div class="col-md-4 mb-3">
                        <div class="card bg-secondary text-white">
                            <div class="card-body">
                                <h5>${p.nombre}</h5>
                                <p>Precio: $${p.precio}<br>Stock: ${p.stock}</p>
                            </div>
                        </div>
                    </div>`;
            });
            html += `</div>`;
            contenedor.innerHTML = html;
        });
}



// 3. FORMULARIO PARA REGISTRAR VENTA (MÉTODO 2: TRANSACCIÓN + TRIGGERS)
function formNuevaVenta() {
    contenedor.innerHTML = `
        <h3>Generar Nueva Venta</h3>
        <div class="card p-4 bg-dark">
            <div class="mb-3">
                <label>ID Cliente:</label>
                <input type="number" id="v_cliente" class="form-control" value="1">
            </div>
            <div class="mb-3">
                <label>ID Producto:</label>
                <input type="number" id="v_producto" class="form-control" value="1">
            </div>
            <div class="mb-3">
                <label>Cantidad:</label>
                <input type="number" id="v_cantidad" class="form-control" value="1">
            </div>
            <div class="mb-3">
                <label>Precio Unitario:</label>
                <input type="number" id="v_precio" class="form-control" value="20">
            </div>
            <button onclick="ejecutarVenta()" class="btn btn-warning">Finalizar Compra</button>
        </div>
    `;
}

function ejecutarVenta() {
    const data = {
        cliente_id: document.getElementById('v_cliente').value,
        producto_id: document.getElementById('v_producto').value,
        cantidad: document.getElementById('v_cantidad').value,
        precio: document.getElementById('v_precio').value
    };

    fetch('/api/realizar-venta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        if (res.status === "success") {
            alert("¡Éxito! " + res.message);
            verInventario(); // Refrescar para ver el trigger en acción
        } else {
            alert("ERROR DE DB: " + res.message); // Aquí saldría el error del Trigger de stock
        }
    });
}



// 4. ESCUCHADORES DE EVENTOS (Conecta con los IDs de tu menú)
// Reemplaza 'id-de-tu-boton' con los IDs reales de tu welcome.html
document.addEventListener('DOMContentLoaded', () => {
    // Ejemplo: Si tu botón de Consultar Opción 1 tiene id="btn-inventario"
    document.getElementById('btn-inventario')?.addEventListener('click', verInventario);
    document.getElementById('btn-reporte-ventas')?.addEventListener('click', verReporteVentas);
    document.getElementById('btn-nueva-venta')?.addEventListener('click', formNuevaVenta);
});
