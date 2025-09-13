import pyscreenshot as ImageGrab
from PIL import Image, ImageFilter

def aplicar_desenfoque_a_imagen(ruta_imagen, ruta_guardado, radio_blur=15):
    """
    Abre una imagen, le aplica un filtro de desenfoque y la guarda.
    """
    try:
        # Cargar la imagen desde la ruta
        img = Image.open(ruta_imagen)

        # Aplicar el filtro de desenfoque (Gaussian Blur)
        # ajustar el radio_blur para controlar la intensidad del desenfoque
        img_borrosa = img.filter(ImageFilter.GaussianBlur(radius=radio_blur))

        # Guardar la imagen desenfocada
        img_borrosa.save(ruta_guardado)
        print(f"Imagen borrosa guardada en: {ruta_guardado}")
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en la ruta '{ruta_imagen}'")
    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen: {e}")

def capturar_y_desenfocar_pantalla(ruta_guardado="captura_borrosa.png", radio_blur=15):
    """
    Realiza una captura de pantalla, le aplica desenfoque y la guarda.
    """
    try:
        # Capturar la pantalla completa
        # se puede especificar un área si es necesario: bbox=(x1, y1, x2, y2)
        imagen_capturada = ImageGrab.grab()
        
        # Guardar la imagen temporalmente para procesarla con Pillow
        ruta_temporal = "captura_temporal.png"
        imagen_capturada.save(ruta_temporal)

        # Aplicar el desenfoque a la imagen capturada
        aplicar_desenfoque_a_imagen(ruta_temporal, ruta_guardado, radio_blur)

        # Eliminar el archivo temporal si no lo necesitas
        import os
        os.remove(ruta_temporal)

    except Exception as e:
        print(f"Ocurrió un error al capturar o procesar la pantalla: {e}")

## Ejemplo de modo de uso ##

# if __name__ == "__main__":
#     capturar_y_desenfocar_pantalla("captura_borrosa.png", 5)
