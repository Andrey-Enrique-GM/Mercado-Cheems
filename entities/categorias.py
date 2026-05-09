from persistence.db import get_connection

class Categorias:
    def __init__(self, id: int = None, nombre: str = '', descripcion: str = ''):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    
    # Metodo para guardar una nueva categoria en la base de datos
    def save(nombre: str, descripcion: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, descripcion))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving category:{ex}")
            return False
