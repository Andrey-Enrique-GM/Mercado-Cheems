from persistence.db import get_connection
from flask_login import UserMixin
from enums.rol import Profile
import pymysql

class Usuarios(UserMixin):
    def __init__(self, id: int, nombre: str, email: str, password_hash: str, is_active: bool, rol: Profile):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self._is_active = is_active
        self.rol = rol


    # Propiedad para obtener el estado de cuenta del usuario (Activo o Inactivo)
    @property
    def is_active(self):
        return self._is_active

        
    # Metodo para guardar un nuevo usuario en la base de datos
    @staticmethod
    def save(nombre: str, email: str, password_hash: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, email, password_hash))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving user:{ex}")
            return False
        