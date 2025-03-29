from conexion.conexion import obtener_cursor

class User:
    def get_user(username, password):
        cursor, conn = obtener_cursor()
        if cursor and conn:
            try:
                cursor.execute("""
                    SELECT COUNT(*) FROM usuario WHERE name = %s AND password = %s;
                """, (username, password))
                result = cursor.fetchone()
                return result[0] > 0  # Retorna True si hay al menos un usuario con esas credenciales
                print("SIIIIIIIIIIIIIIII")
            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        return False



