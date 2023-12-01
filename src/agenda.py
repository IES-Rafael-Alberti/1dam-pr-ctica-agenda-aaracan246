"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}


CONTACTOS_INICIALES = [
    "Laura;Iglesias;liglesias@gmail.com;666777333;666888555;607889988",
    "Antonio;Amargo;aamargo@gmail.com",
    "Marta;Copete;marcopete@gmail.com;+34600888800",
    "Rafael;Ciruelo;rciruelo@gmail.com;+34607212121;655001122",
    "Daniela;Alba;danalba@gmail.com;+34600606060;+34670898934",
    "Rogelio;Rojo;rogrojo@gmail.com;610000099;645000013"]


def pedir_email(contactos: list):

    email = input("Introduzca un email: ")  
    while not email or '@' not in email:
        print("Ese email no es válido.")
        email = input("Introduzca un email: ")  
    return email

def mostrar_agenda_inicial():
    print(CONTACTOS_INICIALES)

def mostrar_menu():

    print("AGENDA")
    print("------")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")



#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()
def pedir_opcion():
    #He creado una función para que el programa te pida una opción de la lista.
    try:
        return int(input("Por favor, elija una opción de la lista: "))
    
    except ValueError:
        print("*** ERROR *** Seleccione un número.")



def agregar_contacto(contactos: list):
    nuevoContacto = {}

    # Aquí pedimos y validamos el nombre y apellido
    #:param_contactos:
    nuevoContacto["nombre"] = input("Ingrese el nombre: ").strip().title()
    nuevoContacto["apellido"] = input("Ingrese el apellido: ").strip().title()

    # Aquí pedimos y validamos el email
    nuevoContacto["email"] = pedir_email(contactos)

    # Pedimos y validamos los teléfonos
    nuevoContacto["telefonos"] = []
    while True:
        telefono = input("Ingrese un número de teléfono (o presione Enter para terminar): ").strip()
        if not telefono:
            break
        if validar_telefono(telefono):
            nuevoContacto["telefonos"].append(telefono)
        else:
            print("Número de teléfono no válido. Inténtelo de nuevo.")

    # Agregar el nuevo contacto a la lista
    contactos.append(nuevoContacto)
    print("Se ha agregado 1 contacto.")


def mostrar_contactos_por_criterio(contactos: list):
    #:param_contactos:
    criterio = input("Introduzca el criterio de búsqueda (nombre, apellido, email o teléfono): ").lower()
    valor = input("Introduzca un valor de búsqueda: ").lower()

    if criterio not in ['nombre', 'apellido', 'email', 'telefonos']:
        print("Ese no es un criterio de búsqueda válido.")
        return

    contactosEncontrados = []
    for contacto in contactos:
        if criterio == 'nombre' and valor in contacto['nombre'].lower():
            contactosEncontrados.append(contacto)

        elif criterio == 'apellido' and valor in contacto['apellido'].lower():
            contactosEncontrados.append(contacto)

        elif criterio == 'email' and valor in contacto['email'].lower():
            contactosEncontrados.append(contacto)

        elif criterio == 'telefonos' and any(valor in telefono for telefono in contacto['telefonos']):
            contactosEncontrados.append(contacto)

    if contactosEncontrados:
        for contacto in contactosEncontrados:
            print(f"Nombre: {contacto['nombre']} {contacto['apellido']} ({contacto['email']})")
            if contacto['telefonos']:
                telefonos = ' / '.join(contacto['telefonos']) 
            else: 
                print(f"Teléfonos: {telefonos}")
                print("......")
    else:
        print("No se han encontrado contactos con ese criterio.")

def modificar_contacto(contactos: list):
    #Aquí se pueden modificar los distintos contactos. 
    #:param_contactos:
    email = input("Introduce el email del contacto que quieres modificar: ")
    contacto = buscar_contacto(contactos, email)

    if contacto:
        print("Contacto encontrado:")
        pos = buscar_contacto(contactos, email)
        print("¿Qué deseas modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. Email")
        print("4. Teléfonos")
        

        opcion = pedir_opcion()

        if opcion == 1:
            nuevo_nombre = input("Nuevo nombre: ").strip().title()
            contacto[pos]["nombre"] = nuevo_nombre
            print("Has modificado el nombre del contacto.")

        elif opcion == 2:
            nuevo_apellido = input("Nuevo apellido: ").strip().title()
            contacto[pos]["apellido"] = nuevo_apellido
            print("Has modificado el apellido del contacto.")

        elif opcion == 3:
            nuevo_email = pedir_email(contactos)
            contacto[pos]["email"] = nuevo_email
            print("Has modificado el email del contacto.")

        elif opcion == 4:
            nuevo_telefonos = []
            while True:
                nuevo_telefono = input("Inserte un nuevo número de teléfono (o presiona Enter para terminar): ").strip()
                if nuevo_telefono == "":
                    break
                if validar_telefono(nuevo_telefono):
                    nuevo_telefonos.append(nuevo_telefono)
                else:
                    print("Número de teléfono no válido.")
            contacto[pos]["telefonos"] = nuevo_telefonos
            
            print("Teléfonos modificados con éxito.")

        else:
            print("Opción no válida.")

    else:
        print("Contacto no encontrado.")


def validar_email(contactos: list, email: str, dupes: bool):
    #Aquí verificamos las distintas formas en las que un email podría no ser correcto.
    #:param_contactos:
    #:param_email:
    #:param_dupes:
    if email == "" or email == " ":
        raise ValueError("El email no puede ser una cadena vacía.")
    if not "@" in email:
        raise ValueError("El email no es un correo válido.")
    if not dupes and buscar_contacto(contactos, email) is not None:
        raise ValueError("El email ya existe en la agenda.")
    return True


def validar_telefono(telefono: str) -> bool:
    #Aquí validamos las distintas opciones que pueden aparecer en un teléfono:
    #:param_telefono:
    if not telefono:
        return False
    
    # Permitir espacios y un posible prefijo +34 // .startswith te permite especificar unos caracteres para un bool.
    telefono = telefono.replace(" ", "")
    if telefono.startswith("+34"):
        telefono = telefono[3:]

    if len(telefono) == 9:
        return True
    
    return False


def buscar_contacto(contactos: list, email: str):
    #He creado una función para que el programa encuentre un contacto mediante el uso de un correo.
    pos = 0
    for contacto in contactos:
        if 'email' in contacto and contacto['email'] == email:
            return pos
        pos += 1  
  




           



def mostrar_contactos(contactos: list):
    #Aquí mostramos la lista de contactos con la agenda completa.
    #:param_contactos:

    print("\nAGENDA")
    print("------")
    for contacto in contactos:
        print(f"Nombre: {contacto['nombre']} {contacto['apellido']}")
        print(f"Email: {contacto['email']}")
        
        if 'telefonos' in contacto:
            print(f"Teléfonos: {', '.join(contacto['telefonos'])}")
        else:
            print("Teléfonos: No disponibles")

        print("\n---")

           


# AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **





def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):
    """ Carga los contactos iniciales de la agenda desde un fichero
    ...
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                checkear_contactos(contactos, linea)
    #Simplemente cargamos varias excepciones para varios posibles errores a la hora de gestionar el archivo:
    except FileNotFoundError:
        print("La ruta del archivo no fue encontrado.")
    except IOError:
        print("Ha habido un error durante la lectura del archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    


def checkear_contactos(contactos: list, linea):
    #Aquí creamos una función para poder registrar que los contactos que se importan luego en cargar_contactos() cumplen los requisitos de lectura.
    #:param_contactos:
    #:param_linea:

    linea = linea.strip().split(';')
    nombre = linea[0]    
    apellido = linea[1]
    email = linea[2]

    telefono = linea[3:]


    datos = {'nombre': nombre, 'apellido': apellido, 'email': email, 'telefonos': telefono}
    contactos.append(datos)

def eliminar_contacto(contactos: list):
    """ Elimina un contacto de la agenda
    ...
    """
    email = input("Introduzca un email para eliminar el contacto: ")
    pos = buscar_contacto(contactos, email)
    
    try:
        if pos is not None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def vaciar_agenda(contactos:list):

    contactos.clear()
    return contactos

def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        conjuntoSimetrico = {8}
        if opcion in OPCIONES_MENU ^ conjuntoSimetrico:
            
                if opcion == 1:
                    borrar_consola()
                    agregar_contacto(contactos)

                elif opcion == 2:
                    borrar_consola()
                    modificar_contacto(contactos)

                elif opcion == 3:
                    borrar_consola()
                    eliminar_contacto(contactos)

                elif opcion == 4:
                    borrar_consola()
                    vaciar_agenda(contactos)
                    borrar_consola()

                elif opcion == 5:
                    borrar_consola()
                    mostrar_agenda_inicial()

                elif opcion == 6:
                    borrar_consola()
                    mostrar_contactos_por_criterio(contactos)
                elif opcion == 7:
                    borrar_consola()
                    mostrar_contactos(contactos)  
        else:
            print("**** ERROR ****")

def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []
    
    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    print("Bienvenidx a la Agendinator3000+, su nuevo asistente de organización de contactos. Por favor, introduzca los datos que le pida el programa.")
    agregar_contacto(contactos)#?)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)#?)
 
    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 

     
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos)#?)


if __name__ == "__main__":
    main()