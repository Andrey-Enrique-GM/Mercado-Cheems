

class Pagos:
    def __init__(self, id: int, orden_id: int, monto: float, metodo_pago: str):
        self.id = id
        self.orden_id = orden_id
        self.monto = monto
        self.metodo_pago = metodo_pago
