from datos import libros, guardar_datos

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
