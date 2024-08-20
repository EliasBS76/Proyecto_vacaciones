import pyodbc
from src.conexion_base import connect_and_execute_query
from src.conexion_base import connect

#----------FUNCION PARA MOSTRAR UNA LISTA DE LOS AUTORES ANTERIORMENTE GUARDADOS
def mostrar_autores():
    autores_existentes="SELECT id,nombre FROM autor"
    conn=connect()
    cursor = conn.cursor()
    try:
        cursor.execute(autores_existentes)
        autores=cursor.fetchall()
        if autores:
            print("AUTORES EXISTENTES")
            for autor in autores:
                print(f"ID:{autor.id},Nombre:{autor.nombre}")
            while True:
                try:
                    id_autor = int(input("Escribe el id que deseas usar"))
                    #Aqui vamos a verificar si el ID existe
                    if any(autor.id==id_autor for autor in autores):
                        print(f"El id fue seleccionado {id_autor}")
                        return id_autor
                        break
                    else :
                        print(f"El id no fue encontrado {id_autor}")
                except ValueError:
                    print("Entrada no valida. por favor , ingresa un numero entero")
        else : 
            print("No se encontraron autores")
    except Exception as e:
        print(f"Error al recuperar los autores{e}")
    finally:
        cursor.close()
        conn.close()

#|------------------------------------FUNCION PARA LLENAR UN AUTOR-------------------------------------------------|

def fill_author_info():
    nombre = input("INNGRESE EL nombre DEL autor: ")
    nacionalidad = input("Ingrese la nacionalidad del autor: ")
    query ="""
    INSERT INTO autor (nombre, nacionalidad)
    OUTPUT INSERTED.id
    VALUES (?, ?);
    """
    conn = connect()
    cursor = conn.cursor()
    try:
        # Ejecutar la consulta de inserción
        cursor.execute(query, (nombre, nacionalidad))
        id_insertado = cursor.fetchone()[0]
        
        # Confirmar la transacción
        conn.commit()

        # Mostrar el ID insertado
        print(f"ID del autor insertado: {id_insertado}")
        return id_insertado
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conn.rollback()  # Deshacer la transacción en caso de error
        raise
    finally:
        cursor.close()
        conn.close()

#|----------------------------------------FUNCION PARA LLENAR UN LIBRO------------------------------------------------------|


def fill_book_info():
    titulo = input("Ingrese el título del libro: ")
    genero = input("Ingrese el género del libro: ")
    precio = int(input("Ingrese el precio del libro: "))
    while True:
        try:
            opc = int(input("SELECCIONA 1 SI DESEAS USAR UN AUTOR YA EXISTENTE O SELECCIONA 2 SI DESEAS CREAR UNO NUEVO: "))
            if opc == 1:
                id_autor=mostrar_autores()
                break
            elif opc == 2:
                id_autor=fill_author_info()
                
                if id_autor is None:
                    print("No se selecciono ningun AUTOR.Intentelo de nuevo")
                    continue
                break
            else:
                print("Opción no válida. Por favor, selecciona 1 o 2.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entero.")
    query = """
        INSERT INTO libro (titulo, genero, precio, autor_id) 
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?)
    """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query,(titulo,genero,precio,id_autor))
        id_libro=cursor.fetchone()[0]
        conn.commit()
        print(f"EL ID DEL LIBRO INSERTADO: {id_libro}")
        return id_libro
    except Exception as e:
        precio(f"ERROR AL OBTENER EL ID DEL LIBRO {e}")
    finally : 
        cursor.close
        conn.close  
    print("Libro añadido exitosamente.")

#|-------------------------------------------FUNCION PARA LLENAR VENTAS---------------------------------------------------|
def fill_sales_info(book_id):
    continente = input("Ingrese el continente donde se realizó la venta: ")
    mes = input("Ingrese el mes de la venta: ")
    venta_mensual = int(input("Ingrese el número de ventas mensuales: "))
    ventas_totales = int(input("Ingrese el número de ventas totales: "))

    query = """
        INSERT INTO ventas (libro_id, continente, mes, venta_mensual, ventas_totales) 
        VALUES (?, ?, ?, ?, ?)
    """
    params = (book_id, continente, mes, venta_mensual, ventas_totales)

    connect_and_execute_query(query, params)
    print("Venta añadida exitosamente.")

#|-------------------------------------------CODIGO INCIAL ----------------------------------------------------|



while True:
    try:
        opc = int(input("BIENVENIDO A LLENADO DE INFORMACIÓN. Presione 1 si desea ingresar un autor , 2 para ingresar un libro: y 3 si dese salir "))
        
        if opc == 1:
            print("Estas ingresando un nuevo autor")
            fill_author_info()

        elif opc == 2:
            print("Estas ingresando un nuevo libro")
            id_libro=fill_book_info()

            
        else:
            print("Opción no válida, por favor intente de nuevo.")
    
    except ValueError:
        print("Favor de seleccionar un número válido.")
