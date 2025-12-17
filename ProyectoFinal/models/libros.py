from datos import libros, guardar_datos
from models.prestamos import prestamos  # Para verificar préstamos activos

def registrar_libro(titulo: str, autor: str, isbn: str) -> bool:
    titulo = titulo.strip()
    autor = autor.strip()
    isbn = isbn.strip()

    if not titulo or not autor or not isbn:
        return False

    if any(l["isbn"] == isbn for l in libros):
        return False

    libros.append({
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "disponible": True
    })
    guardar_datos()
    return True

def obtener_libros() -> list:
    return libros

def obtener_libros_disponibles() -> list:
    return [l for l in libros if l.get("disponible", True)]

def cambiar_estado_libro(isbn: str, disponible: bool) -> bool:
    for libro in libros:
        if libro["isbn"] == isbn:
            libro["disponible"] = disponible
            guardar_datos()
            return True
    return False

# === NUEVAS FUNCIONES ===

def eliminar_libro(isbn: str) -> bool:
    """
    Elimina un libro por ISBN.
    Retorna True si se eliminó, False si está prestado (no se puede eliminar).
    """
    # Verificar si el libro está prestado (activo)
    for p in prestamos:
        if p.get("activo", False) and p["codigo"] == isbn:
            return False  # No se puede eliminar un libro prestado
    
    global libros
    libros = [l for l in libros if l["isbn"] != isbn]
    guardar_datos()
    return True

def actualizar_libro(isbn: str, nuevo_titulo: str, nuevo_autor: str) -> bool:
    """
    Actualiza el título y autor de un libro.
    Retorna True si se actualizó, False si el ISBN no existe o si los datos son inválidos.
    """
    nuevo_titulo = nuevo_titulo.strip()
    nuevo_autor = nuevo_autor.strip()

    if not nuevo_titulo or not nuevo_autor:
        return False

    for libro in libros:
        if libro["isbn"] == isbn:
            libro["titulo"] = nuevo_titulo
            libro["autor"] = nuevo_autor
            guardar_datos()
            return True
    return False
