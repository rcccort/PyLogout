# PyLogout

Una pantalla de salida de sesión simple, elegante y configurable para escritorios Linux basados en GTK3.

`PyLogout` nace como una alternativa moderna a `oblogout`, especialmente para sistemas actualizados (como Debian 13) donde este último puede no ser fácil de instalar. Ofrece una interfaz limpia y es altamente personalizable.

<img title="Captura de PyLogout" src="./Captura.png" alt="Captura de pantalla de PyLogout" width="800">

## Características

*   **Interfaz Limpia:** Pantalla completa sin bordes con un diseño minimalista.
*   **Configurable:** Modifica los comandos de sesión (apagar, reiniciar, etc.) para que se adapten a tu sistema (`systemd`, etc.).
*   **Personalizable:** Cambia fácilmente el fondo, los iconos y los atajos de teclado a través de un archivo de configuración simple.
*   **Fondo Dinámico (Opcional):** Puede tomar una captura de pantalla y aplicarle un efecto de desenfoque para usarla como fondo.
*   **Script de Lanzamiento:** Incluye un script `run.sh` para un inicio fácil y correcto.

## Requisitos

*   Python 3
*   GTK3 y sus dependencias de introspección (PyGObject).
*   Un compositor de ventanas X11.

El resto de las dependencias de Python se gestionan con el archivo `requirements.txt`.

## Instalación

1.  **Clona el Repositorio**
    ```bash
    git clone <URL-de-tu-repositorio>
    cd PyLogout # O el nombre de la carpeta del repositorio
    ```

2.  **Crea y Activa un Entorno Virtual** (Recomendado)
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala las Dependencias**
    Dentro del entorno virtual, instala todo lo necesario con un solo comando:
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: En algunas distribuciones, puede que necesites instalar dependencias del sistema como `build-essential`, `python3-dev`, `libcairo2-dev` o `cmake` si `pip` necesita compilar algo).*

4.  **Ejecuta la Aplicación**
    Usa el script de lanzamiento proporcionado. La primera vez que lo ejecutes, creará el directorio de configuración en `~/.config/pylogout`.
    ```bash
    ./run.sh
    ```
    *(Si el comando falla, asegúrate de que el script tenga permisos de ejecución con `chmod +x run.sh`)*.

## Configuración

Toda la personalización se realiza en el archivo `~/.config/pylogout/pylogout.conf`.

*   **`[layout]`**: Controla qué botones se muestran y en qué orden. Simplemente edita la lista `buttons` para añadir, quitar o reordenar los botones.
*   **`[labels]`**: Edita el texto que aparece debajo de cada botón.
*   **`[commands]`**: Adapta aquí los comandos de apagado, reinicio, etc., a tu sistema. Por defecto, usa `systemctl`, pero puedes cambiarlo a lo que necesites.
*   **`[theme]`**: Cambia la imagen de fondo, los iconos y el color de resaltado del atajo de teclado en las etiquetas (con el valor `highlight_color`). Simplemente coloca tus archivos en las carpetas `~/.config/pylogout/fondo` y `~/.config/pylogout/botones` y actualiza las rutas aquí.
*   **`[shortcuts]`**: Define los atajos de teclado para cada acción.

## Próximos Pasos

-   [x] Implementar los atajos de teclado.
-   [x] Implementar carteles de texto al pie de los botones.
