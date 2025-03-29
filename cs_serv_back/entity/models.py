from conexion.conexion import obtener_cursor


class Productos:
    @staticmethod
    def get_producto(id):
        """ Obtiene un producto por ID si su estado es True. """
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("SELECT * FROM producto WHERE id = %s AND estado = TRUE;", (id,))
                producto = cursor.fetchone()
                return producto
            except Exception as e:
                print(f"Error al obtener el producto: {e}")
            finally:
                cursor.close()
                conn.close()
        return None

    @staticmethod
    def get_productos():
        """ Obtiene todos los productos con estado True. """
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("SELECT * FROM producto WHERE estado = TRUE;")
                productos = cursor.fetchall()
                return productos
            except Exception as e:
                print(f"Error al obtener los productos: {e}")
            finally:
                cursor.close()
                conn.close()
        return []

    @staticmethod
    def delete_producto(id):
        """ Desactiva un producto (cambia estado a False en lugar de eliminarlo). """
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("UPDATE producto SET estado = FALSE WHERE id = %s;", (id,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar el producto: {e}")
            finally:
                cursor.close()
                conn.close()
        return False

    @staticmethod
    def insert_producto(nombre, descripcion, precio, stock):
        """ Inserta un nuevo producto con estado True. """
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("""
                    INSERT INTO producto (nombre, descripcion, precio, stock, estado)
                    VALUES (%s, %s, %s, %s, TRUE)
                    RETURNING id;
                """, (nombre, descripcion, precio, stock))
                nuevo_id = cursor.fetchone()[0]
                conn.commit()
                return nuevo_id
            except Exception as e:
                print(f"Error al insertar el producto: {e}")
            finally:
                cursor.close()
                conn.close()
        return None
    
    @staticmethod
    def update_producto(id, nombre, descripcion, precio, stock):
        """ Actualiza los datos de un producto con estado True. """
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("""
                    UPDATE producto
                    SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                    WHERE id = %s AND estado = TRUE;
                """, (nombre, descripcion, precio, stock, id))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error al actualizar el producto: {e}")
            finally:
                cursor.close()
                conn.close()
        return False


