import json
import os
from datetime import datetime

# Archivos de persistencia
# Archivos de persistencia
DATA_DIR = "data"
LIBROS_FILE = os.path.join(DATA_DIR, "libros.json")
CLIENTES_FILE = os.path.join(DATA_DIR, "clientes.json")
PRESTAMOS_FILE = os.path.join(DATA_DIR, "prestamos.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Listas internas
libros = []
clientes = []
prestamos = []

from models.entities import Cliente

# ---------------- Funciones de persistencia ----------------
def guardar_datos():
    with open(LIBROS_FILE, "w", encoding="utf-8") as f:
        json.dump(libros, f, ensure_ascii=False, indent=4)
    with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
        json.dump([{"nombre": c.nombre, "apellido": c.apellido, "cedula": c.cedula} for c in clientes], f, ensure_ascii=False, indent=4)
    with open(PRESTAMOS_FILE, "w", encoding="utf-8") as f:
        json.dump(prestamos, f, ensure_ascii=False, indent=4)

def cargar_datos():
    # Mutate existing lists instead of replacing them
    libros.clear()
    clientes.clear()
    prestamos.clear()

    if os.path.exists(LIBROS_FILE):
        with open(LIBROS_FILE, "r", encoding="utf-8") as f:
            libros.extend(json.load(f))
    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            clientes_data = json.load(f)
            clientes.extend([Cliente(c["nombre"], c["apellido"], c["cedula"]) for c in clientes_data])
    if os.path.exists(PRESTAMOS_FILE):
        with open(PRESTAMOS_FILE, "r", encoding="utf-8") as f:
            prestamos.extend(json.load(f))
