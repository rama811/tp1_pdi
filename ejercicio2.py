import numpy as np
import cv2
import matplotlib.pyplot as plt

def contador_celdas(image):

    ''' Funcion que recibe la celda donde estan los datos a validar en un determinado renglon del formulario
    y devuelve la cantidad de caracteres y de palabras'''

    # Umbralamos para que nos quede imagen binaria y bien marcadas las letras
    umbralada = image < 110

    # Casteo a uint8 para poder usar connectedComponentsWithStats()
    umbralada = umbralada.astype(np.uint8)

    # detectamos los componentes conectados
    componentes_conectados = cv2.connectedComponentsWithStats(umbralada, 8, cv2.CV_32S)

    stats = componentes_conectados[2]
    
    # Umbralado para que no se cuente como componentes lo que haya quedado de los bordes del campo.
    # En nuestro caso los renglones nos quedaron con grande areas de los bordes, por eso filtramos
    # quedandonos con los elemenos con menor area que son las letras
    area = stats[:, -1] < 200
    stats = stats[area,:]

    # Ordenamos las estadisticas en orden ascendente de acuerdo al elemento [0] (eje x) de cada subarray por que
    # vamos a restar luego en orden:
    indices_ordenados = np.argsort(stats[:, 0])
    stats = stats[indices_ordenados]

    # La cantidad de caracteres son las cantidad de componentes detectados, es decir la cantidad de letras, guiones o barras
    cantidad_caracteres = len(stats)

    if cantidad_caracteres != 0:
        # Si hay mas de un caracter consideramos que en principio hay una palabra
        cantidad_palabras = 1

        for i in range(len(stats)-1):

            # Vamos restando en orden de la siguiente componente a la anterior la diferencia entre los valores
            # del eje x si la diferencia es mayor a determinado umbral entonces es una separacion de palabras
            # y no solo de letras
            if ( stats[i+1][0] - (stats[i][0] + stats[i][2]) ) > 8:
                cantidad_palabras+=1
                cantidad_caracteres+=1

    # Si hay 0 caracteres hay 0 palabras
    else: 
        cantidad_palabras = 0

    # Devolvemos la cantidad de caracteres y palabras del renglon en cuestion
    return cantidad_caracteres, cantidad_palabras


def validacion_formulario(image):

    ''' Funcion que recibe una imagen del formulario como matriz y devuelve la validacion de los campos del
    mismo'''

    # Umbralamos
    img_umbral = img < 110

    # Buscar las columnas externas del formulario:
    # Suma de columnas para encontrarlas:
    img_columnas = np.sum(img_umbral,axis=0)

    # Umbralamos ahora la suma de pixeles, las columnas son las que mas pixeles tienen, con el valor
    # elegido nos va a dar True en las columnas
    img_columnas_umbral = img_columnas > 160

    # Buscamos los valores de los indices en los que estan dichas columnas
    img_cols_indices = np.argwhere(img_columnas_umbral).reshape(1, -1)

    # Repetimos con las filas, para buscar todas los bordes que componen cada una de ellas:
    img_filas = np.sum(img_umbral,axis=1)
    img_filas_umbral = img_filas > 900
    img_filas_indices = np.argwhere(img_filas_umbral).reshape(1, -1)

    # En este diccionario vamos a guardar los resultados de las validaciones
    estadisticas_formulario = {}

    # La idea es ir recorriendo fila a fila
    for j in range(len(img_filas_indices[0])-1):

        numero_renglon = j+1

        # Los renglones 1 y 6 no nos interesan porque no tiene informacion que queremos analizar
        if numero_renglon in [1,6]:
            continue
        else:

            # Si estamos en el renglon de nombre y apellido
            if numero_renglon == 2:
                # Pasamos a contador_celdas() el crop de la celda que nos interesa del renglon en cuestion
                # con las filas correspondientes y siempre nos quedamos con los pixeles de las columnas donde se encuentran
                # los datos (en nuestra lista siempre se guardan en la posicion 1 y 3)
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                # Chequeamos las reestricciones del renglon
                if cantidad_caracteres_renglon <= 25 and cantidad_palabras_renglon >= 2:
                    estadisticas_formulario['nombre_y_apellido']='OK'
                else: estadisticas_formulario['nombre_y_apellido']='MAL'

            # Repetimos lo mismo para cada uno de los renglones con sus respectivas reestricciones
            elif numero_renglon == 3:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon in [2,3] and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['edad']='OK'
                else: estadisticas_formulario['edad']='MAL'

            elif numero_renglon == 4:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon <= 25 and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['mail']='OK'
                else: estadisticas_formulario['mail']='MAL'

            elif numero_renglon == 5:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon == 8 and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['legajo']='OK'
                else: estadisticas_formulario['legajo']='MAL'

            elif numero_renglon == 7:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon == 1 and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['pregunta_1']='OK'
                else: estadisticas_formulario['pregunta_1']='MAL'

            elif numero_renglon == 8:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon == 1 and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['pregunta_2']='OK'
                else: estadisticas_formulario['pregunta_2']='MAL'

            elif numero_renglon == 9:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon == 1 and cantidad_palabras_renglon == 1:
                    estadisticas_formulario['pregunta_3']='OK'
                else: estadisticas_formulario['pregunta_3']='MAL'

            elif numero_renglon == 10:
                cantidad_caracteres_renglon, cantidad_palabras_renglon = contador_celdas( img[ img_filas_indices[0][j]:img_filas_indices[0][j+1], img_cols_indices[0][1]:img_cols_indices[0][3] ] )
                if cantidad_caracteres_renglon <= 25 and cantidad_caracteres_renglon > 0:
                    estadisticas_formulario['comentarios']='OK'
                else: estadisticas_formulario['comentarios']='MAL'

    return estadisticas_formulario

# Leemos la imagen original
img = cv2.imread(r'C:\Users\tomas\OneDrive\Desktop\facultad\4to cuatrimestre\Procesamiento de imagenes\TP1\formulario_01.png', cv2.IMREAD_GRAYSCALE)

# Imprimimos la validacion
print(validacion_formulario(img))
