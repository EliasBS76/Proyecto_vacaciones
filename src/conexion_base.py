import pyodbc

def connect():
    try:
        conn = pyodbc.connect("DRIVER={SQL Server};SERVER=ELIASBS;DATABASE=REPORTE_LIBROS;Trusted_Connection=yes;")
        print("SI SE CONECTÓ A LA BASE.")  # Mensaje para depuración
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

def connect_and_execute_query(query, params):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()  # Asegúrate de llamar a commit() con paréntesis
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        raise
    finally:
        cursor.close()
        conn.close()