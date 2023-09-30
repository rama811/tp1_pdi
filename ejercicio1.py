import cv2

def histograma_ecualizar(image, window_size):

    alto, ancho = image.shape

    # Calcula la mitad del tamaño de la ventana
    tamanio_vent = window_size // 2

    # Crea una copia de la imagen de salida
    imagen_salida = image.copy()

    for y in range(tamanio_vent, alto - tamanio_vent):
        for x in range(tamanio_vent, ancho - tamanio_vent):
            # Extrae la ventana local
            window = image[y - tamanio_vent:y + tamanio_vent + 1, x - tamanio_vent:x + tamanio_vent + 1]

            # Calcula el histograma local
            hist = cv2.calcHist([window], [0], None, [256], [0, 256])

            # Aplica la ecualización del histograma local
            ventana = cv2.equalizeHist(window)

            # Coloca los píxeles ecualizados en la imagen de salida
            imagen_salida[y, x] = ventana[tamanio_vent, tamanio_vent]

    return imagen_salida

# Carga la imagen de entrada
imagen = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

# Aplica la ecualización local del histograma
cv2.namedWindow('Ventana = 20', cv2.WINDOW_NORMAL)
imagen_salida = histograma_ecualizar(imagen,20)
cv2.imshow('Ventana = 20', imagen_salida)

# Tamaño de ventana distinto
cv2.namedWindow('Ventana = 75', cv2.WINDOW_NORMAL)
imagen_salida = histograma_ecualizar(imagen,75)
cv2.imshow('Ventana = 75', imagen_salida)

# Otro tamaño de la ventana
cv2.namedWindow('Ventana = 5', cv2.WINDOW_NORMAL)
imagen_salida = histograma_ecualizar(imagen,5)
cv2.imshow('Ventana = 5', imagen_salida)


cv2.waitKey(0)
cv2.destroyAllWindows()
