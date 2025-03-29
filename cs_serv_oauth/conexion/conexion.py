import psycopg2


def leer_configuracion():
    try:
        with open("../../sec_workspace/BD_ENVIRONMENT.arvl", "r") as f:
            linea = f.readline().strip()
            datos = linea.split("|")
            if len(datos) != 5:
                raise ValueError("Formato de configuración incorrecto")
            return {
                "host": datos[0],
                "port": datos[1],
                "dbname": datos[2],
                "user": datos[3],
                "password": datos[4]
            }
    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        return None


def get_conexion():
    conn = None
    config = leer_configuracion()

    if config:
        try:
            # Conectar a la base de datos
            conn = psycopg2.connect(**config)
            print("Conexión exitosa")
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")
    else:
        print("No se pudo leer la configuración.")
    
    return conn

get_conexion()
