

class Productos:
    def __init__(self, id: int, nombre: str, descripcion: str, precio: float,
                 precio_oferta: float, stock: int, categoria_id: int):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.precio_oferta = precio_oferta
        self.stock = stock
        self.categoria_id = categoria_id
