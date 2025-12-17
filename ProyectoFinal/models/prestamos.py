from datetime import datetime, timedelta
from datos import prestamos, guardar_datos, libros, clientes  # ✅ Añade 'clientes' aquí

def libro_disponible(isbn: str) -> bool:
    for libro in libros:
        if libro["isbn"] == isbn:
            return libro.get("disponible", True)
    return False

def obtener_libro(isbn: str):
    for libro in libros:
        if libro["isbn"] == isbn:
            return libro
    return None

def prestar_libro(codigo_libro: str, cedula_cliente: str, dias_prestamo: int = 7) -> bool:
    # ✅ Valida existencia del cliente directamente (sin importar cliente_existe)
    cliente_valido = any(c.cedula == cedula_cliente for c in clientes)
    if not cliente_valido:
        return False
        
    if not libro_disponible(codigo_libro):
        return False

    fecha_prestamo = datetime.now()
    fecha_limite = fecha_prestamo + timedelta(days=dias_prestamo)

    prestamos.append({
        "codigo": codigo_libro,
        "cedula": cedula_cliente,
        "fecha_prestamo": fecha_prestamo.isoformat(),
        "fecha_limite": fecha_limite.isoformat(),
        "activo": True
    })

    libro = obtener_libro(codigo_libro)
    if libro:
        libro["disponible"] = False

    guardar_datos()
    return True

def devolver_libro(codigo_libro: str) -> bool:
    for prestamo in prestamos:
        if prestamo["codigo"] == codigo_libro and prestamo.get("activo", True):
            prestamo["activo"] = False
            libro = obtener_libro(codigo_libro)
            if libro:
                libro["disponible"] = True
            guardar_datos()
            return True
    return False
