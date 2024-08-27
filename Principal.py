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
        print(f"ERROR AL OBTENER EL ID DEL LIBRO {e}")
    finally : 
        cursor.close()
        conn.close()
    print("Libro añadido exitosamente.")

#|-------------------------------------------FUNCION PARA LLENAR VENTAS---------------------------------------------------|


def ventas(id_libro) : 
    continentes=["AMERICA","AFRICA","ASIA","EUROPA","OCEANIA"]
    while True:
        print("CONTINENTES A LLENAR: ", ", ".join(continentes))
        continente  = input("Escribe el nombre del continente que deseas insertar ")
        continente= continente.upper()
        if continente =="AMERICA":
            llenado_meses(id_libro,continente)

            continentes.remove("AMERICA")

        elif continente =="AFRICA":
            llenado_meses(id_libro,continente)

            continentes.remove("AFRICA")

        elif continente =="ASIA":
            llenado_meses(id_libro,continente)

            continentes.remove("ASIA")

        elif continente =="EUROPA":
            llenado_meses(id_libro,continente)

            continentes.remove("EUROPA")

        elif continente =="OCEANIA":
            llenado_meses(id_libro,continente)

            continentes.remove("OCEANIA")
        else:
            print("OPCION NO VALIDA , FAVOR DE INGRESAR EL NOMBRE DEL CONTINENTE TAL COMO SE LE MUESTRA")
        if not continentes:
            print("TODOS LOS CONTINENTES FUERON LLENADOS :)")
            break

            

def llenado_meses(id_libro,continente):
    enero=int(input("Ingresa las ventas del mes de enero "))
    febrero=int(input("Ingresa las ventas del mes de febreo "))
    marzo=int(input("Ingresa las ventas del mes de marzo "))
    Abril=int(input("Ingresa las ventas del mes de Abril "))
    Mayo=int(input("Ingresa las ventas del mes de Mayo "))
    Junio=int(input("Ingresa las ventas del mes de junio "))
    Julio=int(input("Ingresa las ventas del mes de julio "))
    Agosto=int(input("Ingresa las ventas del mes de Agosto "))
    septiembre=int(input("Ingresa las ventas del mes de Septiembre "))
    octubre=int(input("Ingresa las ventas del mes de Octubre "))
    noviembre=int(input("Ingresa las ventas del mes de Noviembre "))
    diciembre=int(input("Ingresa las ventas del mes de Diciembre "))
    venta_anual = (enero+febrero+marzo+Abril+Mayo+Junio+Julio+Agosto+septiembre+octubre+noviembre+diciembre)
    query = """
    INSERT INTO venta (libro_id,continente,enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre,venta_anual)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

    """
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(query,(id_libro,continente,enero,febrero,marzo,Abril,Mayo,Junio,Julio,Agosto,septiembre,octubre,noviembre,diciembre,venta_anual))
        conn.commit()
    except Exception as e : 
        print(f"ERROR AL EJECUTAR LA CONSULTA : {e}")
    finally:
        cursor.close()
        conn.close()





    
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
            ventas(id_libro)
            
        else:
            print("Opción no válida, por favor intente de nuevo.")
    
    except ValueError:
        print("Favor de seleccionar un número válido.")
