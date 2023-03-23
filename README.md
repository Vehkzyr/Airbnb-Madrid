# Airbnb-Madrid
El objetivo de este trabajo es comprobar si se está utilizando la plataforma Airbnb por parte de empresas, en lugar de particulares, 
para alquiler turístico en el centro de Madrid.

Para la realizacion de las funciones se leer los datos de madrid-airbnb-listings-small.csv

Las funciones son las siguientes: 

# Script functions.py

    1. Extraer del fichero de alojamientos una lista con todos los alojamientos, donde cada alojamiento sea un diccionario que contenga el identificador 
    del alojamiento, el identificador del anfitrión, el distrito, el precio y las plazas.
    
    2. Crear una función que reciba la lista de alojamientos y devuelva el número de alojamientos en cada distrito.
    
    3. Crear una función que reciba la lista de alojamientos y un número de ocupantes y devuelva la lista de alojamientos con un número de plazas mayor o 
    igual que el número de ocupantes.
    
    4. Crear una función que reciba la lista de alojamientos un distrito, y devuelva los 10 alojamientos más baratos del distrito.
    
    5. Crear una función que reciba la lista de alojamientos y devuelva un diccionario con los anfitriones y el número de alojamientos que posee cada uno.

# Script functionsPandas.py:

    1. Preprocesar el fichero de alojamientos para crear un data frame con las variables id, host_id, listing_url, room_type, neighbourhood_group_cleansed,
    price, cleaning_fee, accommodates, minimum_nights, minimum_cost, review_scores_rating, latitude, longitude, is_location_exact. Eliminar del data frame
    cualquier fila incompleta. Añadir al data frame nuevas variables con el coste mínimo por noche y por persona (que incluya los gastos de limpieza).
    
    2. Crear una función que reciba una lista de distritos y devuelva un diccionario con los tipos de alojamiento en ese distrito y el porcentaje de 
    alojamientos de ese tipo.
    
    3. Crear una función que reciba una lista de distritos y devuelva un diccionario con el número de alojamientos que cada anfitrión ofrece en esos 
    distrito, ordenado de más a menos alojamientos.
    
    4. Crear una función que reciba devuelva un diccionario con el número medio de alojamientos por anfitrión de cada distrito.
    
    5. Crear una función que reciba una lista de distritos y dibuje un diagrama de sectores con los porcentajes de tipos de alojamientos en esos distritos.
    
    6. Crear una función que dibuje un diagrama de barras con el número de alojamientos por distritos.
    
    7. Crear una función que dibuje un diagrama de barras con los porcentajes acumulados de tipos de alojamientos por distritos.
    
    8. Crear una función reciba una lista de distritos y una lista de tipos de alojamientos, y dibuje un diagrama de sectores con la distribución del 
    número de alojamientos de ese tipo por anfitrión.
    
    9. Crear una función que dibuje un diagrama de barras con los precios medios por persona y día de cada distrito.
    
    10. Crear una función que reciba una lista de distritos y dibuje un gráfico de dispersión con el coste mínimo por noche y persona y la puntuación en
    esos distritos.
    
