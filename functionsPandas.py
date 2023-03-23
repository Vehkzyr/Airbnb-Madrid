'''
@author Pablo Seijo
@date 21/4/2023
@company USC ETSE
'''

import pandas as pd
from langdetect import detect
import matplotlib.pyplot as plt

'''
@description Preprocesar el fichero de alojamientos para crear un data frame con las variables id, host_id, listing_url, 
            room_type, neighbourhood_group_cleansed, price, cleaning_fee, accommodates, minimum_nights, minimum_cost, review_scores_rating, 
            latitude, longitude, is_location_exact. Eliminar del data frame cualquier fila incompleta. Añadir al data frame nuevas variables 
            con el coste mínimo por noche y por persona (que incluya los gastos de limpieza).
'''
#Basicamente un data frame se trata de una tabla con las filas y las columnas del .csv
try:
    data = pd.read_csv('madrid-airbnb-listings-small.csv', sep = '\t')

except FileNotFoundError:
    print('ERROR: File not found')

else:
    # Renombramos los nombres de las columnas que queremos
    # #inplace = True es un parámetro que se puede utilizar en varias funciones de Pandas, como dropna(), drop(), fillna(),
    #entre otras. Cuando se establece a True, se modifica el objeto DataFrame original en lugar de devolver una copia del objeto modificado.
    data.rename(columns={'host_id': 'propietario', 'listing_url': 'url', 'room_type': 'tipo_alojamiento',
                                     'neighbourhood_group_cleansed': 'distrito', 'price': 'precio',
                                     'cleaning_fee': 'gastos_limpieza', 'accommodates': 'plazas',
                                     'minimum_nights': 'noches_minimas', 'review_scores_rating': 'puntuacion', 'name': 'nombre'}, inplace = True)

    # Filtramos las columnas que queremos
    data = data[ ['id', 'propietario', 'url', 'tipo_alojamiento', 'distrito', 'precio', 'gastos_limpieza', 'plazas',
             'noches_minimas', 'puntuacion', 'nombre']]

    # Eliminamos las filas con valores NaN
    data = data.dropna()

    # Eliminamos el carácter $ de las columnas del precio y gastos_limpieza y las convertimos a float
    # con str[1:] obviamos el primer caracter del string ($) y cogemos solo el numero para despues convertirlo a float con astype
    # qeu convierte la/s variables que ke indiquemos al tipo de dato que le indiquemos
    data['precio'] = data.precio.str.replace(',', '').str[1:].astype('float')
    data['gastos_limpieza'] = data.gastos_limpieza.str[1:].astype('float')

    # Creamos una nueva columna con el precio por persona multiplicando el precio diario por el número mínimo de noches, sumando los gastos de limpieza y finalmente dividiendo por el número mínimo de noches y el número de plazas.
    # Con round redondeamos a dos decimales para que quede un precio mas exacto
    data['precio_persona'] = round( (data.precio * data.noches_minimas + data.gastos_limpieza) / (data.noches_minimas + data.plazas), 2)


####################################### - FUNCIONES - ##################################################################
'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@param distritos: Es una lista con los nombres de los distritos. 
@description Función que devuelve una serie con el porcentaje de tipos de alojamientos en una lista de distritos dada.
@return Una serie con el porcentaje de tipos de alojamientos en los distritos dados.
'''
def tiposAlojamientoDistrito(alojamientos, distritos):

    # Filtramos los alojamientos a los distritos seleccionados cogiendo los alojamientos que estan dentro de los distritos que le pasamos
    # poniendo alojamientos.distritos obtenemos el distrito de cada alojamiento de la lista, y comprabamos si estan en la lista pasada
    # como argumentos
    alojamientos = alojamientos[alojamientos.distrito.isin(distritos)]

    # Hacemos el porcentaje de tipo de alojamiento, value_counts cuenta las veces que aparace un valor unico en cada tabla,
    # normalize hace el porcentajes en valores de 0 a 1 y lo multiplicampos por 100 para devolver el porcentaje real
    alojamientos = alojamientos.tipo_alojamiento.value_counts(normalize = True) * 100

    return alojamientos

'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@param distritos: Es una lista con los nombres de los distritos. 
@description Crear una función que reciba una lista de distritos y devuelva un diccionario con el número de alojamientos 
            que cada anfitrión ofrece en esos distrito, ordenado de más a menos alojamientos.
@return devuelva un diccionario con el número de alojamientos que cada anfitrión ofrece en esos distrito, ordenado de más a menos alojamientos.
'''
def alojamientosPropietariosDistritos(alojamientos, distritos):

    #Primero filtramos los alojamientos por los distritos seleccionados
    alojamientos = alojamientos[alojamientos.distrito.isin(distritos)]

    #Seleccionamos el numero de apartamentos que tiene cada propietario en los distritos seleccionados
    alojamientos = alojamientos.propietario.value_counts()

    #Y finalmente ordenamos de mayor a menor numero de propiedades
    alojamientos = alojamientos.sort_values(ascending = True)

    return alojamientos

'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@param distritos: Es una lista con los nombres de los distritos. 
@description Crear una función que reciba una lista de alojamientos devuelva un diccionario con el número medio de alojamientos por anfitrión de cada distrito
@return devuelva un diccionario con el número medio de alojamientos por anfitrión de cada distrito
'''
def mediaAlojamientosDistrito(alojamientos):

    #Agrupamos los alojamientos por distrito con groupby
    alojamientos = alojamientos.groupby('distrito')

    #Contamos las propiedades de cada propietario con value_counts de nuevo
    alojamientos = alojamientos.propietario.value_counts()

    # El método unstack() en un objeto pandas DataFrame se utiliza para desapilar (convertir) una de las etiquetas de índice (inde
    # x) de nivel inferior a las columnas. En este caso, se supone que level = "distrito" especifica que el índice de nivel
    # inferior "distrito" será desapilado y convertido en columnas.
    # Después de desapilar los datos, el método mean() calcula el valor medio para cada una de las columnas. El resultado será
    # un objeto pandas Series con el valor medio para cada columna que antes formaba parte del nivel "distrito" del índice.
    alojamientos = alojamientos.unstack(level = 'distrito').mean()

    return round(alojamientos, 6)


'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@param distritos: Es una lista con los nombres de los distritos. 
@description Crear una función que reciba una lista de distritos y dibuje un diagrama de sectores con los porcentajes de tipos de alojamientos en esos distritos.
@return devuelva un png con un diagrama de sectores
'''
def diagramaPieTipos (alojamientos, distritos):

    #definimos la figura y los ejes del grafico
    fig, ax = plt.subplots()

    # ajustamos el tamaño de la figura
    fig.set_size_inches(15, 15)

    #llamamos a la funcion tiposAlojamientoDistrito para que nos de los tipos de alojamiento por distrito
    alojamientos = tiposAlojamientoDistrito(alojamientos,distritos)

    #Dibujamos el diagrama de sectores
    alojamientos.plot(kind = 'pie')

    # Ponermos el título, con el + ', ' .join(distritos) imprimo los distritos que se le pasa
    ax.set_title('Distribución del porcentaje de tipos de alojamientos\n Distritos de ' + ', '.join(distritos), loc = "center")

    #Eliminamos el eje y
    ax.set_ylabel('')

    #Guardamos la figura
    plt.savefig('TiposAlojamientoPorDistito.png')

    print('SUCCESS: Figura guardada correctamente')

    return

'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@description Crear una función que dibuje un diagrama de barras con el número de alojamientos por distritos.
@return devuelva un png con un diagrama de sectores
'''
def NumAlojamientosDistrito(alojamientos):

    # definimos una lista de colores
    colors = ['blue', 'green', 'red', 'purple', 'orange']

    #definimos la figura y los ejes del grafico
    fig, ax = plt.subplots()

    # ajustamos el tamaño de la figura
    fig.set_size_inches(15, 15)

    #Dibujamos el diagrama de barras
    alojamientos.distrito.value_counts().plot(kind = 'bar', color = colors)

    # Ponermos el título, con el + ', ' .join(distritos) imprimo los distritos que se le pasa
    ax.set_title('Numero de alojamientos por distrito', loc = 'center')

    # Ponemos una rejilla al fondo de la grafica, en el eje y de color gris claro y linea discontinua
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')

    #Guardamos la figura
    plt.savefig('CantidadAlojamientosDistrito.png')

    print('SUCCESS: Figura guardada correctamente')

    return


'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@description Crear una función que dibuje un diagrama de barras con los porcentajes acumulados de tipos de alojamientos por distritos.
@return devuelva un png con un diagrama con los tipo
'''
def diagramaBarrasDistrito (alojamientos):

    # definimos una lista de colores
    colors = ['blue', 'green', 'red', 'purple', 'orange']

    #definimos la figura y los ejes del grafico
    fig, ax = plt.subplots()

    #ajustamos el tamaño de la figura
    fig.set_size_inches(15, 15)

    # Calculamos el pocentaje de los tipos alojamientos en cada distrito
    alojamientos = alojamientos.groupby('distrito').tipo_alojamiento.value_counts(normalize = True) * 100

    # Dibujamos el diagrama de barras
    alojamientos.unstack().plot(kind = 'bar', stacked = True, ax = ax)

    # Ponermos el título, con el + ', ' .join(distritos) imprimo los distritos que se le pasa
    ax.set_title('Tipos de alojamiento por distrito', loc = 'center')

    # Ponemos una rejilla al fondo de la grafica, en el eje y de color gris claro y linea discontinua
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')

    # Añadimos la legenda
    plt.legend(loc = 'best')

    # Eliminamos el eje y
    ax.set_xlabel('')

    #Guardamos la figura
    plt.savefig('TiposAlojamientoDistritoBarras.png')

    print('SUCCESS: Figura guardada correctamente')

    return


'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@description Crear una función que dibuje un diagrama de barras con los precios medios por persona y día de cada distrito.
@return devuelva un png con un diagrama de barras
'''
def diagramaBarrasPrecioPersona (alojamientos):

    # definimos una lista de colores
    colors = ['blue', 'green', 'red', 'purple', 'orange']

    #definimos la figura y los ejes del grafico
    fig, ax = plt.subplots()

    #ajustamos el tamaño de la figura
    fig.set_size_inches(15, 15)

    # Agrupamos los alojamientos por distrito
    alojamientos = alojamientos.groupby('distrito')

    #realizamos la grafica ( recorddemos que .mean() nos calcula la media aritmetica  )
    alojamientos = alojamientos['precio_persona'].mean().plot(kind = 'bar', color = colors)

    # Ponermos el título, con el + ', ' .join(distritos) imprimo los distritos que se le pasa
    ax.set_title('Precio medio persona', loc = 'center')

    # Ponemos una rejilla al fondo de la grafica, en el eje y de color gris claro y linea discontinua
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')

    #Guardamos la figura
    plt.savefig('PreciosDistrito.png')

    print('SUCCESS: Figura guardada correctamente')

    return

'''
@param alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
@param distritos: Es una lista con los nombres de los distritos. 
@description Crear una función que reciba una lista de distritos y dibuje un gráfico de dispersión con el coste mínimo por noche 
            y persona y la puntuación en esos distritos.
@return devuelva un png con un diagrama de barras
'''
def diagramaDispersionCosteMin (alojamientos, distritos):
    # Creamos una lista de colores para los puntos
    colors = ['aquamarine', 'navy', 'cyan', 'lightseagreen', 'darkviolet']

    #definimos la figura y los ejes del grafico
    fig, ax = plt.subplots()


    #filtramos la lista de alojamientos a los distritos seleccionados
    alojamientos = alojamientos[alojamientos.distrito.isin(distritos)]

    # Repite la lista de colores en bloques de 5 para poder meterlos en el grafico de diperssion
    colors = (colors * (len(alojamientos) // 5 + 1))[:len(alojamientos)]

    # Calculamos el precio por persona
    alojamientos['precio_persona'] = (alojamientos.precio * alojamientos.noches_minimas + alojamientos.gastos_limpieza) / (alojamientos.noches_minimas + alojamientos.plazas)

    #utlizamos .scatter() para hacer un diagrama de dispersion de la lista de alojamientos
    ax.scatter(x = alojamientos['precio_persona'], y = alojamientos['puntuacion'], c = colors)

    # Ponermos el título, con el + ', ' .join(distritos) imprimo los distritos que se le pasa
    ax.set_title('Precio y Puntuacion por distritos', loc = 'center')

    # Ponemos una rejilla al fondo de la grafica, en el eje y de color gris claro y linea discontinua
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')
    ax.grid(axis = 'x', color='lightgray', linestyle='dashed')

    # Añadimos la legenda
    plt.legend(loc = 'best')

    #Ponemos nombre a x e y
    ax.set_xlabel('Precio'); ax.set_ylabel('Puntuacion')

    #Guardamos la figura
    plt.savefig('PreciosPuntuacionDistritos.png')

    print('SUCCESS: Figura guardada correctamente')

    return

diagramaDispersionCosteMin(data, ['Centro','Villaverde', 'Vicálvaro'])
diagramaBarrasPrecioPersona(data)
diagramaBarrasDistrito(data)
diagramaPieTipos(data,['Centro','Villaverde', 'Vicálvaro'])
NumAlojamientosDistrito(data)