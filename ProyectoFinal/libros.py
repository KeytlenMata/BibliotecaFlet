"""
Módulo de Libros

Responsabilidades:
- Registro de libros
- Visualización del inventario
- Validación de datos
- Prevención de duplicados por ISBN
"""

from datos import libros, libro_existe, guardar_datos


def registrar_libro(titulo: str, autor: str, isbn: str) -> bool:
    """
    Registra un nuevo libro en el sistema.

    Parámetros:
    - titulo (str): Título del libro
    - autor (str): Autor del libro
    - isbn (str): Código ISBN único

    Retorna:
    - True si el libro se registra correctamente
    - False si hay campos vacíos o el ISBN ya existe
    """

    if not titulo or not autor or not isbn:
        return False

    if libro_existe(isbn):
        return False

    libros.append({
        "titulo": titulo.strip(),
        "autor": autor.strip(),
        "codigo": isbn.strip(),
        "disponible": True
    })

    guardar_datos()
    return True


def obtener_libros() -> list:
    """
    Retorna la lista completa del inventario de libros.
    """
    return libros
