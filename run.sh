#!/bin/bash

# Obtiene el directorio donde se encuentra el script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define las rutas al intérprete de Python y al script de la aplicación
VENV_PYTHON="$SCRIPT_DIR/bin/python"
PYLOGOUT_SCRIPT="$SCRIPT_DIR/pylogout.py"

# Se cambia al directorio del script y ejecuta la aplicación
# Esto asegura que las rutas relativas dentro del script de Python funcionen correctamente
cd "$SCRIPT_DIR"
"$VENV_PYTHON" "$PYLOGOUT_SCRIPT"
