/**
 * MERCADO CHEEMS - Lógica de Dashboard y Persistencia
 * Conecta los botones del menú con los métodos de Python/MySQL
 */

const contenedor = document.getElementById('contenedor-principal');



// 1. FUNCIÓN PARA MOSTRAR INVENTARIO COMPLETO (VIEW + SUBQUERIES)
function verInventarioCompleto() {
    fetch('/api/inventario-completo')
        .then(res => res.json())
        .then(data => {
            let html = `
                <h3>Inventario Completo</h3>
                <p class="text-muted">Vista completa con información de productos y veces vendido (Uso de VIEW y SUBQUERIES)</p>
                <div class="table-responsive">
                    <table class="table table-dark">
                        <thead>
                            <tr><th>ID</th><th>Producto</th><th>Precio</th><th>Stock</th><th>Categoría</th><th>Veces Vendido</th></tr>
                        </thead>
                        <tbody>`;
            data.forEach(p => {
                html += `<tr><td>${p.id}</td><td>${p.nombre}</td><td>$${p.precio}</td><td>${p.stock}</td><td>${p.categoria_nombre}</td><td>${p.veces_vendido}</td></tr>`;
            });
            html += `</tbody></table></div>`;
            contenedor.innerHTML = html;
        });
}



// 2. FUNCIÓN PARA MOSTRAR REPORTE DE RESUMEN DE VENTAS (JOIN + GROUP BY + HAVING)
function verReporteResumenVentas() {
    fetch('/api/reporte-resumen-ventas')
        .then(res => res.json())
        .then(data => {
            let html = `
                <h3>Resumen de Ventas</h3>
                <p class="text-muted">Clientes con compras mayores a $100 (Uso de JOIN, GROUP BY, HAVING y ORDER BY)</p>
                <table class="table table-dark">
                    <thead>
                        <tr><th>Cliente</th><th>Total Compras</th><th>Total Gastado</th></tr>
                    </thead>
                    <tbody>`;
            data.forEach(r => {
                html += `<tr><td>${r.nombre}</td><td>${r.total_compras}</td><td>$${r.total_gastado}</td></tr>`;
            });
            html += `</tbody></table>`;
            contenedor.innerHTML = html;
        });
}



// 3. FORMULARIO PARA REALIZAR VENTA (TRANSACCIÓN + TRIGGERS)
function formNuevaVenta() {
    contenedor.innerHTML = `
        <h3>Generar Nueva Venta</h3>
        <p class="text-muted">Formulario para registrar una nueva venta (Uso de TRANSACCIÓN y TRIGGERS)</p>
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
            verInventarioCompleto(); // Refrescar inventario
        } else {
            alert("ERROR: " + res.message);
        }
    });
}



// 4. FORMULARIO PARA BUSCAR CLIENTE (LIKE)
function formBuscarCliente() {
    contenedor.innerHTML = `
        <h3>Buscar Cliente</h3>
        <p class="text-muted">Busca clientes por nombre (Uso de LIKE)</p>
        <div class="card p-4 bg-dark">
            <div class="mb-3">
                <label>Término de búsqueda:</label>
                <input type="text" id="busqueda_cliente" class="form-control" placeholder="Nombre del cliente">
            </div>
            <button onclick="buscarCliente()" class="btn btn-info">Buscar</button>
            <div id="resultados-busqueda" class="mt-3"></div>
        </div>
    `;
}

function buscarCliente() {
    const termino = document.getElementById('busqueda_cliente').value;
    fetch(`/api/buscar-cliente?termino=${encodeURIComponent(termino)}`)
        .then(res => res.json())
        .then(data => {
            let html = '<h5>Resultados:</h5>';
            if (data.length === 0) {
                html += '<p class="text-muted">No se encontraron clientes.</p>';
            } else {
                html += '<table class="table table-dark"><thead><tr><th>Nombre</th><th>Email</th></tr></thead><tbody>';
                data.forEach(c => {
                    html += `<tr><td>${c.nombre}</td><td>${c.email}</td></tr>`;
                });
                html += '</tbody></table>';
            }
            document.getElementById('resultados-busqueda').innerHTML = html;
        });
}



// 5. ESCUCHADORES DE EVENTOS
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn-inventario-completo')?.addEventListener('click', verInventarioCompleto);
    document.getElementById('btn-reporte-resumen-ventas')?.addEventListener('click', verReporteResumenVentas);
    document.getElementById('btn-nueva-venta')?.addEventListener('click', formNuevaVenta);
    document.getElementById('btn-buscar-cliente')?.addEventListener('click', formBuscarCliente);
});
