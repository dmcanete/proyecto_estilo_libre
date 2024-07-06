from app.database import get_db

class Cliente:
    def __init__(self, id_cliente=None, nombre=None, apellido=None, correo=None, telefono=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def get_by_id_cliente(cliente_id):
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (cliente_id,))
            row = cursor.fetchone()
            
            if row:
                cliente = Cliente(
                    id_cliente=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    correo=row[3],
                    telefono=row[4]
                )
                return cliente
            else:
                return None
        
        except Exception as e:
            print(f"Error al obtener cliente por ID: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def get_all():
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            
            clientes = [Cliente(id_cliente=row[0], nombre=row[1], apellido=row[2], correo=row[3], telefono=row[4]) for row in rows]
            return clientes
        
        except Exception as e:
            print(f"Error al obtener todos los clientes: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def save(self):
        try:
            db = get_db()
            cursor = db.cursor()

            if self.id_cliente:
                cursor.execute("UPDATE clientes SET nombre = %s, apellido = %s, correo = %s, telefono = %s WHERE id_cliente = %s",
                               (self.nombre, self.apellido, self.correo, self.telefono, self.id_cliente))
            else:
                cursor.execute("INSERT INTO clientes (nombre, apellido, correo, telefono) VALUES (%s, %s, %s, %s)",
                               (self.nombre, self.apellido, self.correo, self.telefono))
                self.id_cliente = cursor.lastrowid
            
            db.commit()
        
        except Exception as e:
            db.rollback()
            raise e
        
        finally:
            if cursor:
                cursor.close()

    def delete(self):
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (self.id_cliente,))
            db.commit()
        
        except Exception as e:
            db.rollback()
            raise e
        
        finally:
            if cursor:
                cursor.close()

    def serialize(self):
        return {
            'id': self.id_cliente,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
        }
