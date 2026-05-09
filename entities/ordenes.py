

class Ordenes:
    def __init__(self, id: int, cliente_id: int, usuario_id: int, total: float, is_active):
        self.id = id
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.total = total
        self.is_active = is_active
