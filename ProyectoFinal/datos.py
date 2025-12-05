# datos.py

import json
import os
from datetime import datetime, timedelta

# -----------------------------
# ARCHIVOS DE PERSISTENCIA
# -----------------------------
LIBROS_FILE = "libros.json"
CLIENTES_FILE = "clientes.json"
PRESTAMOS_FILE = "prestamos.json"

# -----------------------------
# ESTRUCTURAS GLOBALES EN MEMORIA
# -----------------------------
# Cada lista se inicializa vacía y se carga desde JSON al inicio
libros = []      # dict: {"titulo": str, "autor": str, "codigo": str, "disponible": bool}
clientes = []    # dict: {"nombre": str, "apellido": str, "cedula": str}
prestamos = []   # dict: {"codigo": str, "cedula": str, "fecha_prestamo": datetime, "fecha_limite": datetime}

# -----------------------------
# FUNCIONES DE PERSISTENCIA
# -----------------------------

def cargar_datos():
    """Carga los datos desde los archivos JSON al inicio de la aplicación."""
    global libros, clientes, prestamos
    try:
        # Cargar libros
        if os.path.exists(LIBROS_FILE):
            with open(LIBROS_FILE, "r", encoding="utf-8") as f:
                libros = json.load(f)
        else:
            libros = []

        # Cargar clientes
        if os.path.exists(CLIENTES_FILE):
            with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
                clientes = json.load(f)
        else:
            clientes = []

        # Cargar préstamos
        if os.path.exists(PRESTAMOS_FILE):
            with open(PRESTAMOS_FILE, "r", encoding="utf-8") as f:
                prestamos = json.load(f)
            # Convertir fechas de string a datetime
            for p in prestamos:
                p["fecha_prestamo"] = datetime.fromisoformat(p["fecha_prestamo"])
                p["fecha_limite"] = datetime.fromisoformat(p["fecha_limite"])
        else:
            prestamos = []

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"⚠️ Advertencia: archivo JSON corrupto o formato inválido. Se reinician los datos. Error: {e}")
        libros, clientes, prestamos = [], [], []
    except Exception as e:
        print(f"⚠️ Error inesperado al cargar datos: {e}")
        libros, clientes, prestamos = [], [], []


def guardar_datos():
    """Guarda los datos actuales en los archivos JSON."""
    try:
        # Guardar libros
        with open(LIBROS_FILE, "w", encoding="utf-8") as f:
            json.dump(libros, f, ensure_ascii=False, indent=4)

        # Guardar clientes
        with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(clientes, f, ensure_ascii=False, indent=4)

        # Guardar préstamos (serializar fechas)
        prestamos_serial = []
        for p in prestamos:
            p_copy = p.copy()
            p_copy["fecha_prestamo"] = p["fecha_prestamo"].isoformat()
            p_copy["fecha_limite"] = p["fecha_limite"].isoformat()
            prestamos_serial.append(p_copy)

        with open(PRESTAMOS_FILE, "w", encoding="utf-8") as f:
            json.dump(prestamos_serial, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")


# -----------------------------
# FUNCIONES AUXILIARES DE VALIDACIÓN
# -----------------------------

def libro_existe(codigo: str) -> bool:
    """Devuelve True si ya existe un libro con ese código."""
    return any(libro["codigo"] == codigo for libro in libros)


def cliente_existe(cedula: str) -> bool:
    """Devuelve True si ya existe un cliente con esa cédula."""
    return any(cliente["cedula"] == cedula for cliente in clientes)


def libro_disponible(codigo: str) -> bool:
    """Devuelve True si el libro existe y está disponible."""
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro["disponible"]
    return False


def obtener_libro(codigo: str):
    """Devuelve el diccionario del libro por código, o None si no existe."""
    return next((l for l in libros if l["codigo"] == codigo), None)


def obtener_cliente(cedula: str):
    """Devuelve el diccionario del cliente por cédula, o None si no existe."""
    return next((c for c in clientes if c["cedula"] == cedula), None)