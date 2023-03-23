'''
@author Pablo Seijo
@date 15/4/2023
@company USC ETSE
@description El objetivo de este trabajo es comprobar si se está utilizando la plataforma Airbnb por parte de empresas,
en lugar de particulares, para alquiler turístico en el centro de Madrid.
'''

import csv

#Extraer del fichero de alojamientos una lista con todos los alojamientos, donde cada alojamiento sea un diccionario
# que contenga el identificador del alojamiento, el identificador del anfitrión, el distrito, el precio y las plazas.

# Definir el dialecto para el archivo csv
dialect = csv.excel_tab

try:
    # Abrir el archivo y leer su contenido como un objeto CSV con el dialecto especificado
    with open('madrid-airbnb-listings-small.csv') as lector_csv:
        data = csv.reader(lector_csv, dialect=dialect)
        # Salta la primera fila, de tal manera que desplaza el puntero alamcenando la primera fila en una instancia
        encabezado = next(lector_csv)

        # Almacenamos los valores del encabezado que guardamos en la variable encabezado
        listaEncabezado = encabezado.split('\t')

        # Crear una lista vacía para almacenar los alojamientos
        alojamientos = []

        # Recorrer las filas del archivo y extraer los campos que nos interesan para cada alojamiento
        for row in data:
            #Hacemos un diccionario con los datos de tal manera que podremos acceder a ellos a traves del nombre de la columna
            aloj = {
                'id': row[listaEncabezado.index('id')],
                'id_anfitrion': row[listaEncabezado.index('host_id')],
                'distrito': row[listaEncabezado.index('neighbourhood')],
                'precio': row[listaEncabezado.index('price')],
                'plazas': row[listaEncabezado.index('accommodates')]
            }
            alojamientos.append(aloj)

#Si el archivo no se encuentra salta la excepcion FileNotFoundError que imprime por pontalla eso mismo
except FileNotFoundError:
    print('ERROR: File not found')

####################################### - FUNCIONES - ##################################################################
'''
@param array[alojamiento{diccionario}] alojamientos
@description Crear una función que reciba la lista de alojamientos y devuelva el número de alojamientos en cada distrito.
'''
def alojamientosDistritos (alojamientos):
    #creamos el array que contendra los distritos
    distritos = []

    #Metemos los distritos dentro del array para despues contarlos
    for alojamiento in alojamientos:
        distritos.append(alojamiento['distrito'])

    # Creamos el diccionario para almacenar los resultados
    conteoDistritos = {}

    # Recorremos los elementos del array de distritos
    for distrito in distritos:
        # Si el distrito aún no está en el diccionario, lo agregamos y lo inicializamos a 1
        if distrito not in conteoDistritos:
            conteoDistritos[distrito] = 1
        # Si el distrito ya está en el diccionario, aumentamos su contador en 1
        else:
            conteoDistritos[distrito] += 1

    return conteoDistritos

'''
@param array[alojamiento{diccionario}] alojamientos
@param int numOcupantes
@description Crear una función que reciba la lista de alojamientos y un número de ocupantes y devuelva la lista de 
            alojamientos con un número de plazas mayor o igual que el número de ocupantes.
'''
def disponibilidadAlojamiento(alojamientos, ocupantes):

    #hago un arraya auxiliar para copiar los alojamientos con plazas disponibles
    alojamientosDisponibles = []

    for alojamiento in alojamientos:
        #casteo el dato a int y compruebo
        if(int(alojamiento['plazas']) >= ocupantes):
            alojamientosDisponibles.append(alojamiento)

    return alojamientosDisponibles

'''
@param array[alojamiento{diccionario}] alojamientos: lista de alojamientos 
@param string distrito: distrito a estudiar
@param int cant: cantidad a devolver
@description Crear una función que reciba la lista de alojamientos un distrito, y devuelva los Cant alojamientos más baratos del distrito.
'''
def alojamientosBaratos(alojamientos, distrito, cant):

    # Filtramos los alojamientos del distrito
    alojamientosDistrito = [alojamiento for alojamiento in alojamientos if alojamiento['distrito'] == distrito]

    # Ordeno los alojamientos por precio de menor a mayor
    # Gracias a la funcion sorted que ordena listas, y su funcion para recorrer en funcion de claves se puede realizar de manera muy sencilla
    # lambda x es una forma de crear una función anónima (es decir, sin nombre) en Python. En este caso, se utiliza para definir una función
    # que toma un argumento x y devuelve un valor. En la función sorted(), se utiliza key=lambda x: int(x['precio']) para indicar que se debe
    # ordenar la lista de alojamientos por el precio de cada alojamiento. poniendo [1:] obvio el simbolo del dolar y cojo solo el precio
    alojamientosOrdenados = sorted(alojamientosDistrito, key = lambda x : float(x['precio'][1:]))

    # Devuelvo los cant primeros alojamientos (los más baratos)
    return alojamientosOrdenados[:cant]

'''
@param array[alojamiento{diccionario}] alojamientos: lista de alojamientos 
@description Crear una función que reciba la lista de alojamientos y devuelva un diccionario con los anfitriones y el
            número de alojamientos que posee cada uno.
'''
def landlords (alojamientos):

    #Hago un diccionario de datos para meter a los landlords con sus respectivas casas (recordemos que los diccionarios de datos
    #se hacen con los corchetes
    propietarios = []

    # Metemos los anfitriones dentro del array para despues contarlos
    for alojamiento in alojamientos:
        propietarios.append(alojamiento['id_anfitrion'])

    conteoPropietarios = {}

    # Recorremos los elementos del array de distritos
    for propietario in propietarios:
        # Si el distrito aún no está en el diccionario, lo agregamos y lo inicializamos a 1
        if propietario not in conteoPropietarios:
            conteoPropietarios[propietario] = 1

        # Si el distrito ya está en el diccionario, aumentamos su contador en 1
        else:
            conteoPropietarios[propietario] += 1

    return conteoPropietarios