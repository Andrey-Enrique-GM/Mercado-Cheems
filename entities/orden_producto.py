

class OrdenProducto:
    def __init__(self, id: int, orden_id: int, producto_id: int, cantidad: int, precio: float):
        self.id = id
        self.orden_id = orden_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio = precio
